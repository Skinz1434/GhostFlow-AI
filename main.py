import os
from dotenv import load_dotenv
import openai
import stripe
from fastapi import FastAPI

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
stripe.api_key = os.getenv("STRIPE_KEY")

app = FastAPI()

@app.get("/")
async def status():
    return {"status": "GhostFlow AI operational!"}
