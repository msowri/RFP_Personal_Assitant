from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Not used now , in future we can add authentication and logging middlewares here at this place
def create_app() -> FastAPI:
    app = FastAPI(title="FPA Personal Assistant API", version="1.0.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app