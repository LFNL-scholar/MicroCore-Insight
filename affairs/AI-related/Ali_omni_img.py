import os
import yaml 
import base64
from openai import OpenAI

def encode_image(image_path):
    """Encode local image to base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def main():

    with open('config.yaml', 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)

    client = OpenAI(
        api_key=config['api_key'],
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    # Initialize conversation history
    messages = [
        {
            "role": "system",
            "content": [{"type": "text", "text": "You are a helpful assistant."}],
        }
    ]

    print("Welcome to the Qwen Omni Turbo chat! (Type 'quit' to exit)")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == 'quit':
            break
            
        # Check if user wants to upload an image
        if user_input.lower().startswith('upload'):
            try:
                image_path = input("Please enter the path to the image: ").strip()
                if not os.path.exists(image_path):
                    print("Error: File not found.")
                    continue
                    
                # Encode the image
                base64_image = encode_image(image_path)
                image_url = f"data:image/jpeg;base64,{base64_image}"
                
                # Add image to messages
                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url},
                        },
                        {"type": "text", "text": "Describe this image"},
                    ],
                })
            except Exception as e:
                print(f"Error processing image: {e}")
                continue
        else:
            # Regular text message
            messages.append({
                "role": "user",
                "content": [{"type": "text", "text": user_input}],
            })

        # Get response from the model
        completion = client.chat.completions.create(
            model="qwen-omni-turbo",
            messages=messages,
            modalities=["text"],
            stream=True,
            stream_options={"include_usage": True}
        )

        print("\nAssistant: ", end="", flush=True)
        assistant_response = ""
        
        for chunk in completion:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                if content:
                    print(content, end="", flush=True)
                    assistant_response += content
        
        # Add assistant response to conversation history
        if assistant_response:
            messages.append({
                "role": "assistant",
                "content": [{"type": "text", "text": assistant_response}],
            })

if __name__ == "__main__":
    main()