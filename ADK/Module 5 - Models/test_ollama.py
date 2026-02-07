import requests
from pprint import pprint

headers = {
    'Content-Type': 'application/json',
}

data = {
    "model": "llama3.2",  # Ensure this is the correct model name for Llama 3.2
    "messages": [
        {"role": "user", "content": "Hello Ollama, are you running?"}
    ]
}

# Replace 'localhost' with your actual Ollama server address if different
response = requests.post('http://localhost:11434/v1/chat/completions', headers=headers, json=data)


# Print the below with proper json formatting in terminal
pprint(response.json())

if response.status_code == 200:
    print("Success! Llama 3.2 is running on Ollama.")
    print("Response:", response.json())
else:
    print("Error! Status code:", response.status_code)
    print("Details:", response.text)
