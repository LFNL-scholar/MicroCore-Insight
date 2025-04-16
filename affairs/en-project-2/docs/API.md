# API Documentation

本文档描述了语音服务的 API 接口，包括语音识别（ASR）和语音合成（TTS）两个主要功能。

## 目录

- [ASR API](#asr-speech-recognition-api) - 语音识别接口
- [TTS API](#text-to-speech-api) - 语音合成接口

## Text to Speech API

将文本转换为语音的 API 接口。

### 请求信息

- **URL**: `/api/tts`
- **Method**: `POST`
- **Content-Type**: `application/json`

### 请求参数

| 参数名 | 类型   | 必填 | 描述         | 限制 |
|--------|--------|------|--------------|------|
| text   | string | 是   | 要转换为语音的文本 | 不能为空，最大长度100字符 |
| voice  | string | 是   | 语音音色 | 指定要使用的语音音色 |

> 音色列表：https://www.volcengine.com/docs/6561/1257544

### 请求示例

```json
{
    "text": "你好，世界",
    "voice": "zh_female_wanwanxiaohe_moon_bigtts"
}
```

### 响应参数

| 参数名     | 类型   | 描述         |
|------------|--------|--------------|
| status     | string | 请求状态，成功为 "success" |
| message    | string | 响应消息     |
| audio_data | string | Base64 编码的音频数据 |

### 响应示例

```json
{
    "status": "success",
    "message": "语音合成成功",
    "audio_data": "base64编码的音频数据..."
}
```

### 错误响应

当发生错误时，API 将返回以下格式的响应：

```json
{
    "detail": "错误信息"
}
```

| HTTP 状态码 | 描述         | 可能的原因 |
|-------------|--------------|------------|
| 200         | 请求成功     | - |
| 400         | 请求参数错误 | 文本为空或超过100字符 |
| 500         | 服务器内部错误 | 服务器处理过程中发生异常 |

### 错误示例

```json
{
    "detail": "文本不能为空"
}
```

```json
{
    "detail": "文本不能超过100个字符"
}
```

### 注意事项

1. audio_data 字段包含 Base64 编码的 MP3 格式音频数据
2. 客户端需要将 Base64 数据解码后才能播放或保存为音频文件
3. 文本长度限制为100个字符，超过会返回400错误
4. 需要指定正确的语音音色（voice参数）

### 使用示例

#### cURL
```bash
curl -X POST "http://localhost:8007/api/tts" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "你好，世界",
       "voice": "zh_female_wanwanxiaohe_moon_bigtts"
     }'
```

#### Python
```python
import requests
import base64

url = "http://localhost:8007/api/tts"
data = {
    "text": "你好，世界",
    "voice": "zh_female_wanwanxiaohe_moon_bigtts"
}

response = requests.post(url, json=data)
if response.status_code == 200:
    result = response.json()
    audio_data = base64.b64decode(result["audio_data"])
    # 保存为音频文件
    with open("output.mp3", "wb") as f:
        f.write(audio_data)
else:
    print(f"Error: {response.json()['detail']}")
```

## ASR (Speech Recognition) API

将语音转换为文本的 API 接口。

### 请求信息

- **URL**: `/api/asr`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`

### 请求参数

| 参数名 | 类型   | 必填 | 描述         | 限制 |
|--------|--------|------|--------------|------|
| audio_file | File | 是   | MP3格式的音频文件 | 文件大小不超过10MB |

### 请求示例

```bash
curl -X POST "http://localhost:8007/api/asr" \
     -H "Content-Type: multipart/form-data" \
     -F "audio_file=@/path/to/your/audio.mp3"
```

### 响应参数

| 参数名     | 类型   | 描述         |
|------------|--------|--------------|
| status     | string | 请求状态，成功为 "success" |
| message    | string | 响应消息     |
| text       | string | 识别出的文本内容 |

### 响应示例

```json
{
    "status": "success",
    "message": "语音识别成功",
    "text": "识别出的文本内容"
}
```

### 错误响应

当发生错误时，API 将返回以下格式的响应：

```json
{
    "detail": "错误信息"
}
```

| HTTP 状态码 | 描述         | 可能的原因 |
|-------------|--------------|------------|
| 200         | 请求成功     | - |
| 400         | 请求参数错误 | 非MP3格式文件、文件为空、文件过大 |
| 500         | 服务器内部错误 | 语音识别失败或其他服务器异常 |

### 错误示例

```json
{
    "detail": "只支持MP3格式的音频文件"
}
```

```json
{
    "detail": "音频文件不能超过10MB"
}
```

### 注意事项

1. 仅支持 MP3 格式的音频文件
2. 文件大小限制为 10MB
3. 音频文件不能为空

### 使用示例

#### Python
```python
import requests

url = "http://localhost:8007/api/asr"
audio_file_path = "path/to/your/audio.mp3"

with open(audio_file_path, "rb") as f:
    files = {"audio_file": ("audio.mp3", f, "audio/mpeg")}
    response = requests.post(url, files=files)

if response.status_code == 200:
    result = response.json()
    print(f"识别结果: {result['text']}")
else:
    print(f"Error: {response.json()['detail']}")
```
