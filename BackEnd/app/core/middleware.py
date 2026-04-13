from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#not used now , feature will be rearhitecture
def create_app() -> FastAPI:
    app = FastAPI(title="FPA Personal Assistant API", version="1.0.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app