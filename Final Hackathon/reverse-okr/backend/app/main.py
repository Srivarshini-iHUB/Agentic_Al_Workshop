from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.agents import router as agents_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agents_router, prefix="/api")