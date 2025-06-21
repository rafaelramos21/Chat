import os
from dotenv import load_dotenv
from fastapi import FastAPI
from stream_chat import StreamChat
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
import models.album
from routers import album


load_dotenv()

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, substitua por domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Roteador dos álbuns e fotos
app.include_router(album.router)

# Configuração do StreamChat
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

# Chamada ao iniciar o app
criar_usuarios_no_stream()

# Rota para gerar token do usuário no chat
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
