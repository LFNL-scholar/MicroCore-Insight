# TTS Service API Documentation

## Text to Speech API

将文本转换为语音的 API 接口。

### 请求信息

- **URL**: `/api/tts`
- **Method**: `POST`
- **Content-Type**: `application/json`

### 请求参数

| 参数名 | 类型   | 必填 | 描述         |
|--------|--------|------|--------------|
| text   | string | 是   | 要转换为语音的文本 |

### 请求示例

```json
{
    "text": "你好，世界"
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
    "message": "成功接收到TTS数据",
    "audio_data": "base64编码的音频数据..."
}
```

### 错误响应

当发生错误时，API 将返回以下格式的响应：

```json
{
    "detail": "服务器内部错误: 错误详情"
}
```

| HTTP 状态码 | 描述         |
|-------------|--------------|
| 200         | 请求成功     |
| 500         | 服务器内部错误 |

### 注意事项

1. audio_data 字段包含 Base64 编码的 MP3 格式音频数据
2. 客户端需要将 Base64 数据解码后才能播放或保存为音频文件
3. 建议对较长文本进行分段处理，避免单次请求文本过长

### 使用示例

#### cURL
```bash
curl -X POST "http://localhost:8007/api/tts" \
     -H "Content-Type: application/json" \
     -d '{"text": "你好，世界"}'
```

#### Python
```python
import requests
import base64

url = "http://localhost:8007/api/tts"
data = {"text": "你好，世界"}

response = requests.post(url, json=data)
if response.status_code == 200:
    result = response.json()
    audio_data = base64.b64decode(result["audio_data"])
    # 保存为音频文件
    with open("output.mp3", "wb") as f:
        f.write(audio_data)
```
