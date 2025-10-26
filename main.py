# ============================================
# Telegram Username ⇄ ID Converter API
# Made by @EskedarEjigu
# ============================================

from fastapi import FastAPI, Query
from telethon import TelegramClient
import re
import asyncio

app = FastAPI()

# === Your Telegram API credentials ===
API_ID = 21166612        # replace with your api_id
API_HASH = "66f91326c15d44606bde39ffaea06422"

# === Create a temporary MTProto client ===
# (We’ll connect only when needed)
async def get_client():
    client = TelegramClient('session', API_ID, API_HASH)
    await client.start()
    return client

@app.get("/")
def home():
    return {"message": "Welcome to Username ⇄ ID API by @EskedarEjigu"}

@app.get("/convert")
async def convert(query: str = Query(..., description="Telegram username or user ID")):
    query = query.strip()
    try:
        client = await get_client()

        if query.startswith('@'):
            user = await client.get_entity(query)
            await client.disconnect()
            return {"username": query, "id": user.id}

        elif re.fullmatch(r'\d+', query):
            user = await client.get_entity(int(query))
            await client.disconnect()
            username = f"@{user.username}" if user.username else None
            return {"id": query, "username": username}

        else:
            await client.disconnect()
            return {"error": "Invalid input. Send @username or numeric user ID."}

    except Exception as e:
        return {"error": str(e)}
