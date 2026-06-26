import os
from fastapi import FastAPI, Request
import httpx

app = FastAPI()

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.post("/")
async def main(request: Request):
    body = await request.json()
    user_text = body.get("request", {}).get("original_utterance", "")

    if not user_text:
        return {
            "version": body.get("version", "1.0"),
            "session": body.get("session"),
            "response": {"text": "Я не расслышала вопрос. Повторите, пожалуйста."}
        }

    if not OPENROUTER_API_KEY:
        return {
            "version": body.get("version", "1.0"),
            "session": body.get("session"),
            "response": {"text": "Извините, API-ключ OpenRouter не настроен."}
        }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openrouter/free",
        "messages": [{"role": "user", "content": user_text}],
        "max_tokens": 500,
        "temperature": 0.7
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(OPENROUTER_API_URL, headers=headers, json=payload)
            response_data = response.json()

            if "error" in response_data:
                error_msg = response_data["error"].get("message", "Неизвестная ошибка")
                answer = f"Ошибка OpenRouter: {error_msg}"
            else:
                # Извлекаем текст, даже если он None
                answer = response_data.get("choices", [{}])[0].get("message", {}).get("content")
                # Если ответ пустой или None, подставляем заглушку
                if not answer:
                    answer = "Извините, я не смогла сформулировать ответ. Попробуйте переформулировать вопрос."
    except httpx.TimeoutException:
        answer = "Превышено время ожидания ответа от OpenRouter. Попробуйте позже."
    except Exception as e:
        answer = f"Произошла ошибка при обращении к OpenRouter: {str(e)}"

    return {
        "version": body.get("version", "1.0"),
        "session": body.get("session"),
        "response": {
            "end_session": False,
            "text": answer
        }
    }

@app.get("/")
async def root():
    return {"message": "Сервер работает, но ожидает POST-запросы"}
