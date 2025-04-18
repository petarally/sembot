from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
import uvicorn
from .router import ChatbotRouter

# Inicijalizacija FastAPI aplikacije
app = FastAPI(title="Fakultetski Chatbot")

# Inicijalizacija Chatbot routera
chatbot_router = ChatbotRouter()

# Model za zahtjev chatbota
class ChatRequest(BaseModel):
    query: str

# Model za odgovor chatbota
class ChatResponse(BaseModel):
    answer: str

# API endpoint za chatbot
@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Endpoint za chatbot upite"""
    response = await chatbot_router.get_response(request.query)
    return ChatResponse(answer=response)

# Omogući CORS za razvoj
@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

# Root endpoint za provjeru da API radi
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Fakultetski Chatbot API</title>
        </head>
        <body>
            <h1>Fakultetski Chatbot API</h1>
            <p>API je aktivan. Koristite /api/chat endpoint za interakciju s chatbotom.</p>
        </body>
    </html>
    """

# Ako se pokreće direktno
if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)