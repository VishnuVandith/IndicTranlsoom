from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time
import logging
from fastapi import FastAPI
import sys

logger = logging.getLogger()

formatter = logging.Formatter(fmt="%(lineno)d - %(asctime)s - %(message)s")

#create handlers

stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("app.log")

#set formatters
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

#add handlers to loggers
logger.handlers = [stream_handler, file_handler]


logger.setLevel(logging.INFO)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Middleware for logging requests and responses
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Log request details
        logging.info(f"Request: {request.method} {request.url}")

        # Call the next middleware/endpoint
        response = await call_next(request)

        # Log response details
        process_time = (time.time() - start_time) * 1000
        formatted_process_time = f"{process_time:.2f} ms"
        logging.info(f"Response: {response.status_code} ({formatted_process_time})")

        return response

app = FastAPI()

# Add the logging middleware to the FastAPI app
app.add_middleware(LoggingMiddleware)
