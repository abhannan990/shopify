from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize the FastAPI app
app = FastAPI()

# Import the router from webhook.py and include it in the app
from .webhook import router as webhook_router
app.include_router(webhook_router)
