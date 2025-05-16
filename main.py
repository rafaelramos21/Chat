import os
from dotenv import load_dotenv
from fastapi import FastAPI
from stream_chat import StreamChat
from fastapi.middleware.cors import CORSMiddleware

# Carrega as variáveis do arquivo .env
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # para teste pode liberar todos, depois restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("STREAM_API_KEY")
API_SECRET = os.getenv("STREAM_API_SECRET")

client = StreamChat(api_key=API_KEY, api_secret=API_SECRET)

# Usuários fixos
USUARIOS_FIXOS = {
    "user_rafael": "Rafael",
    "user_julia": "Julia"
}

def criar_usuarios_no_stream():
    for user_id, user_name in USUARIOS_FIXOS.items():
        client.upsert_user({"id": user_id, "name": user_name})

# Chama essa função ao iniciar o app (ou chame em outro endpoint de setup)
criar_usuarios_no_stream()

@app.get("/token/{user_id}")
def get_token(user_id: str):
    if user_id not in USUARIOS_FIXOS:
        return {"error": "Usuário inválido"}

    token = client.create_token(user_id)
    return {
        "token": token,
        "user": {
            "id": user_id,
            "name": USUARIOS_FIXOS[user_id]
        },
        "api_key": API_KEY
    }
