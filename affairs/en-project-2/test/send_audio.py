import requests

url = "http://localhost:8007/api/asr"
audio_file = 'F:/MicroCore-Insight/affairs/en-project-2/test/output/tts_20250416_132238.mp3'
files = {
    'audio_file': (audio_file, open(audio_file, 'rb'), 'audio/mpeg')
}
response = requests.post(url, files=files)
result = response.json()
print(result)