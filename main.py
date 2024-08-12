# transloom-dev/app/main.py
from fastapi import FastAPI
from api.middleware.cors import configure_cors
from api.middleware.logging import LoggingMiddleware
from api.middleware.auth import BasicAuthMiddleware
from api.endpoints import indicTranslator


# Fast API init
app = FastAPI(
    title="Transloom API",
    description="API for language translation project with TTS, STT, and Swagger UI",
    version="1.0.0",
    debug=True
)

# Middleware

configure_cors(app)
app.add_middleware(LoggingMiddleware)


# Api Routes
app.include_router(indicTranslator.router,prefix="/indicTranslator")

@app.get("/")
async def root():
    return {"message": "Welcome to the Transloom API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
