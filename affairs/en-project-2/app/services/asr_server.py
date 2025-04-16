import time
import os
import uuid
import websockets
import json
import gzip
import asyncio
import base64

# Constants for message types and flags
CLIENT_FULL_REQUEST = 0b0001
CLIENT_AUDIO_ONLY_REQUEST = 0b0010
NO_SEQUENCE = 0b0000
NEG_SEQUENCE = 0b0010
SERVER_FULL_RESPONSE = 0b1001
SERVER_ACK = 0b1011
SERVER_ERROR_RESPONSE = 0b1111
NO_SERIALIZATION = 0b0000
JSON = 0b0001
CUSTOM_TYPE = 0b1111
NO_COMPRESSION = 0b0000
GZIP = 0b0001

# Configuration
appid = "1040131635"
access_token = "Lcv7ShPi4sA7YwLCPqfzT9qlp27vLAQC"
cluster = "volcengine_input_common"
host = "openspeech.bytedance.com"
ws_url = f"wss://{host}/api/v2/asr"
SUCCESS_CODE = 1000


def parse_response(res):
    """Parse the response from ASR server."""
    protocol_version = res[0] >> 4
    header_size = res[0] & 0x0f
    message_type = res[1] >> 4
    message_type_specific_flags = res[1] & 0x0f
    serialization_method = res[2] >> 4
    message_compression = res[2] & 0x0f
    reserved = res[3]
    header_extensions = res[4:header_size * 4]
    payload = res[header_size * 4:]
    result = {}
    payload_msg = None
    payload_size = 0

    if message_type == SERVER_FULL_RESPONSE:
        payload_size = int.from_bytes(payload[:4], "big", signed=True)
        payload_msg = payload[4:]
    elif message_type == SERVER_ACK:
        seq = int.from_bytes(payload[:4], "big", signed=True)
        result['seq'] = seq
        if len(payload) >= 8:
            payload_size = int.from_bytes(payload[4:8], "big", signed=False)
            payload_msg = payload[8:]
    elif message_type == SERVER_ERROR_RESPONSE:
        code = int.from_bytes(payload[:4], "big", signed=False)
        result['code'] = code
        payload_size = int.from_bytes(payload[4:8], "big", signed=False)
        payload_msg = payload[8:]

    if payload_msg is None:
        return result

    if message_compression == GZIP:
        payload_msg = gzip.decompress(payload_msg)
    if serialization_method == JSON:
        payload_msg = json.loads(str(payload_msg, "utf-8"))
    elif serialization_method != NO_SERIALIZATION:
        payload_msg = str(payload_msg, "utf-8")

    result['payload_msg'] = payload_msg
    result['payload_size'] = payload_size
    return result


def generate_header(message_type=CLIENT_FULL_REQUEST, message_type_specific_flags=NO_SEQUENCE):
    """Generate protocol header."""
    header = bytearray()
    header_size = 1
    header.append((0b0001 << 4) | header_size)  # Protocol version
    header.append((message_type << 4) | message_type_specific_flags)
    header.append((0b0001 << 4) | 0b0001)  # JSON serialization & GZIP compression
    header.append(0x00)  # reserved
    return header


def construct_request(reqid, audio_data: bytes):
    """Construct the request payload with audio data."""
    return {
        "app": {
            "appid": appid,
            "cluster": cluster,
            "token": access_token,
        },
        "user": {
            "uid": str(uuid.uuid4()),
        },
        "request": {
            "reqid": reqid,
            "show_utterances": True,
            "sequence": 1
        },
        "audio": {
            "format": "mp3",
            "rate": 16000,
            "language": "zh-CN",
            "bits": 16,
            "channel": 1,
            "codec": "raw",
            "enable_vad": True,
            "enable_punc": True,
            "enable_itn": True,
            "data": base64.b64encode(audio_data).decode('utf-8')  # 将音频数据编码为base64
        },
    }


def slice_data(data: bytes, chunk_size: int):
    """
    将数据切片
    :param data: 音频数据
    :param chunk_size: 分片大小
    :return: (chunk, is_last)
    """
    data_len = len(data)
    offset = 0
    while offset + chunk_size < data_len:
        yield data[offset: offset + chunk_size], False
        offset += chunk_size
    else:
        yield data[offset: data_len], True


async def recognize_speech(audio_data: bytes) -> str:
    """
    将MP3音频数据转换为文字。

    Args:
        audio_data (bytes): MP3格式的音频数据

    Returns:
        str: 识别出的文字，失败返回None
    """
    try:
        auth_header = {'Authorization': f'Bearer; {access_token}'}
        print(f"Audio data size: {len(audio_data)} bytes")
        
        async with websockets.connect(ws_url, additional_headers=auth_header, ping_interval=None) as websocket:
            # 准备请求数据
            reqid = str(uuid.uuid4())
            request_params = construct_request(reqid, audio_data)
            print("Sending request with audio data...")
            
            # 发送请求
            payload_bytes = str.encode(json.dumps(request_params))
            payload_bytes = gzip.compress(payload_bytes)
            
            # 构建并发送请求
            full_request = bytearray()
            full_request.append((0b0001 << 4) | 1)  # Protocol version & header size
            full_request.append((CLIENT_FULL_REQUEST << 4) | NO_SEQUENCE)  # Message type & flags
            full_request.append((JSON << 4) | GZIP)  # Serialization & compression
            full_request.append(0x00)  # Reserved
            full_request.extend((len(payload_bytes)).to_bytes(4, 'big'))
            full_request.extend(payload_bytes)

            await websocket.send(full_request)
            print("Request sent, waiting for response...")

            # 等待识别结果
            start_time = time.time()
            while True:
                try:
                    response = await websocket.recv()
                    result = parse_response(response)
                    print("Response received:", json.dumps(result, indent=2))
                    
                    if 'payload_msg' in result:
                        if result['payload_msg'].get('code') == SUCCESS_CODE:
                            if result['payload_msg'].get('result') and len(result['payload_msg']['result']) > 0:
                                text = result['payload_msg']['result'][0].get("text", "")
                                if text:
                                    print(f"Recognition time: {time.time() - start_time:.3f}s")
                                    return text
                        else:
                            print(f"Recognition failed with code: {result['payload_msg'].get('code')}")
                            return None
                except websockets.exceptions.ConnectionClosed:
                    print("Connection closed by server")
                    break
                except Exception as e:
                    print(f"Error receiving response: {e}")
                    break
            
            return None

    except Exception as e:
        print(f"ASR request failed: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return None


if __name__ == '__main__':
    # 使用示例
    async def test_asr():
        # 读取MP3文件
        with open("F:/MicroCore-Insight/affairs/en-project-2/test/output/tts_20250416_132238.mp3", "rb") as f:
            audio_data = f.read()
        
        # 识别语音
        text = await recognize_speech(audio_data)
        if text:
            print(f"识别结果: {text}")
        else:
            print("识别失败")

    asyncio.run(test_asr())

