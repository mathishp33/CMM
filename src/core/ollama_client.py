import requests

def prompt_model(prompt: str, file_content: str, model: str) -> str:
    messages = [
        {
            "role": "system",
            "content": prompt,
        },
        {
            "role": "user",
            "content": file_content,
        },
    ]

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": model,
            "messages": messages,
            "stream": False,
            "think": False,
            "keep_alive": "30m",
            "options": {
                "temperature": 0,
                "num_predict": 4096,
                "seed": 42,
            },
        },
        timeout=3600,
    )

    response.raise_for_status()

    data = response.json()

    if "error" in data:
        raise RuntimeError(data["error"])

    return data["message"]["content"]