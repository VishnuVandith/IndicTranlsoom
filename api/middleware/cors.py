from fastapi.middleware.cors import CORSMiddleware

def configure_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins
        allow_credentials=True,
        allow_methods=["*"],  # All HTTP methods
        allow_headers=["*"],  # All headers
    )
