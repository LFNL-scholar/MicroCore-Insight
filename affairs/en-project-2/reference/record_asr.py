import websocket
import ssl
import threading
import pyaudio
import json
import gzip
import time
import uuid

# 配置参数
APP_ID = "1040131635"
ACCESS_TOKEN = "Lcv7ShPi4sA7YwLCPqfzT9qlp27vLAQC"
CLUSTER = "volcengine_input_common"
WS_URL = "wss://openspeech.bytedance.com/api/v2/asr"

# 麦克风采样参数
RATE = 16000
CHANNELS = 1
CHUNK = 960  # 60ms
FORMAT = pyaudio.paInt16

# 自定义协议常量
CLIENT_FULL_REQUEST = 0b0001
CLIENT_AUDIO_ONLY_REQUEST = 0b0010
NEG_SEQUENCE = 0b0010

JSON = 0b0001
GZIP = 0b0001

# 构造协议头
def generate_header(message_type=CLIENT_FULL_REQUEST, flags=0b0000):
    header = bytearray()
    header_size = 1
    header.append((0b0001 << 4) | header_size)
    header.append((message_type << 4) | flags)
    header.append((JSON << 4) | GZIP)
    header.append(0x00)
    return header

# 构造初始化 JSON 请求体
def construct_request():
    req = {
        "app": {
            "appid": APP_ID,
            "cluster": CLUSTER,
            "token": ACCESS_TOKEN,
        },
        "user": {
            "uid": str(uuid.uuid4())
        },
        "request": {
            "reqid": str(uuid.uuid4()),
            "show_utterances": False,
            "sequence": 1
        },
        "audio": {
            "format": "raw",
            "rate": 16000,
            "language": "zh-CN",
            "bits": 16,
            "channel": 1,
            "codec": "raw",
        },
    }
    payload = json.dumps(req).encode("utf-8")
    return gzip.compress(payload)

# 录音线程并发送音频数据
def record_audio(ws):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    print("🎤 开始录音...")

    try:
        # 构造并发送初始化请求
        init_payload = construct_request()
        header = generate_header(CLIENT_FULL_REQUEST)
        header.extend(len(init_payload).to_bytes(4, "big"))
        header.extend(init_payload)
        ws.send(header, opcode=websocket.ABNF.OPCODE_BINARY)

        # 连续发送音频流
        while True:
            data = stream.read(CHUNK)
            compressed = gzip.compress(data)
            header = generate_header(CLIENT_AUDIO_ONLY_REQUEST)
            header.extend(len(compressed).to_bytes(4, "big"))
            header.extend(compressed)
            ws.send(header, opcode=websocket.ABNF.OPCODE_BINARY)
    except Exception as e:
        print("❌ 录音结束:", e)
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

def on_message(ws, message):
    try:
        # 解码响应
        if isinstance(message, bytes) and len(message) > 4:
            payload = message[4:]
            try:
                decompressed = gzip.decompress(payload)
                msg = json.loads(decompressed.decode("utf-8"))
                if "result" in msg and len(msg["result"]) > 0:
                    print("🔥 识别结果:", msg["result"][0].get("text", ""))
            except Exception as e:
                print("⚠️ 解码失败:", e)
    except Exception as e:
        print("⚠️ 响应处理异常:", e)

def on_error(ws, error):
    print("❌ 错误:", error)

def on_close(ws, close_status_code, close_msg):
    print("🔚 连接关闭:", close_msg)

def on_open(ws):
    threading.Thread(target=record_audio, args=(ws,), daemon=True).start()

if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(WS_URL,
                                 on_open=on_open,
                                 on_message=on_message,
                                 on_error=on_error,
                                 on_close=on_close)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
