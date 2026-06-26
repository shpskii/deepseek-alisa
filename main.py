from fastapi import FastAPI, Request
import json

app = FastAPI()

@app.post("/")
async def main(request: Request):
    # Получаем тело запроса от Алисы
    data = await request.json()
    
    # Формируем корректный ответ
    response = {
        "version": data.get("version", "1.0"),  # берём версию из запроса или ставим "1.0"
        "session": data.get("session"),          # возвращаем ту же сессию
        "response": {
            "text": "Привет! Я временно работаю в тестовом режиме."
        }
    }
    return response

@app.get("/")
async def root():
    return {"message": "Сервер работает, но ожидает POST-запросы"}
