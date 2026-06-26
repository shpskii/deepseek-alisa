from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/")
async def main(request: Request):
    # Тестовый ответ без вызова DeepSeek
    return {"response": {"text": "Привет! Я временно работаю в тестовом режиме."}}

@app.get("/")
async def root():
    return {"message": "Сервер работает, но ожидает POST-запросы"}
