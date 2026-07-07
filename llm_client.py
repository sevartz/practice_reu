import requests
import config


def ask(system_prompt: str, user_prompt: str,
        max_tokens: int = 800, temperature: float = 0.3) -> str:
    """Задать модели вопрос и вернуть текст ответа.

    system_prompt — задаёт роль/тон («ты дружелюбный помощник покупателя»).
    user_prompt   — собственно данные/просьба.
    temperature   — 0.3 для стабильных ответов (лучше кэшируются).
    """
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
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": 1.0,
        "stream": False,
    }

    response = requests.post(config.NVIDIA_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
