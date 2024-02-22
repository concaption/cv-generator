"""
path: app/main.py
"""
import logging
import colorlog
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.config import settings

from app.routers import main
def configure_logging():
    """
    Configure logging for the application
    """
    # Create a root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    if not root_logger.handlers:
        # Create a formatter for formatting log messages
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            log_colors={
                'DEBUG':    'cyan',
                'INFO':     'green',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'red,bg_white',
            }
        )

        # Create a handler for logging to stdout
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)

        # Add the handlers to the root logger
        root_logger.addHandler(stream_handler)


configure_logging()




app = FastAPI(title=settings.PROJECT_NAME, version="0.1.0", description="Generate CVs using ASI CV Generator")

app.include_router(main.router)
origins = [
    "*",  # Allow all origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
# Configure your secret key
app.add_middleware(SessionMiddleware, secret_key="your-secret-key-here")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)