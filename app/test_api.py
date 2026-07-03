import requests

url = "http://57.159.31.11/v1/chat/completions"

payload = {
    "model": "yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF",
    "messages": [
        {
            "role": "user",
            "content": "Hello"
        }
    ]
}

try:
    response = requests.post(url, json=payload, timeout=10)
    print(response.status_code)
    print(response.text)

except Exception as e:
    print(e)