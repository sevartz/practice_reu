import requests
import config


def ask(system_prompt: str, user_prompt: str,
        max_tokens: int = 800, temperature: float = 0.3) -> str:
    if not config.NVIDIA_API_KEY:
        return "(LLM недоступна: не задан ключ NVIDIA_API_KEY в .env)"

    headers = {
        "Authorization": f"Bearer {config.NVIDIA_API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    payload = {
        "model": config.NVIDIA_MODEL,
        "messages": [
            {"role": "system", "content": "detailed thinking off\n\n" + system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": 0.95,
        "stream": False,
    }

    response = requests.post(config.NVIDIA_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()

    message = data["choices"][0]["message"]
    content = message.get("content") or message.get("reasoning_content") or ""
    return content.strip()