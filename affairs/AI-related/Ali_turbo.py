import os
import yaml 
from openai import OpenAI
import datetime

GREEN = '\033[92m'
END = '\033[0m'

with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

client = OpenAI(
    api_key=config['api_key'],
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

prompt = config['prompt']

messages = [
    {'role': 'system', 'content': prompt}
]

while True:
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_input = input(f"{GREEN}{current_time}{END} LF: ")
    if user_input.lower() == '/bye':
        break

    messages.append({'role': 'user', 'content': user_input})
    completion = client.chat.completions.create(
        model="qwen-turbo-latest",  
        messages=messages,
        stream=True  
    )

    response_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{GREEN}{response_time}{END} AI: ", end="")
    response = ""

    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            response += content
    print()
    
    messages.append({'role': 'assistant', 'content': response})