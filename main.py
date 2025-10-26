# ============================================
# Telegram Username ⇄ ID Converter API
# Fully async + in-memory (Vercel-ready)
# Made by @EskedarEjigu
# ============================================

from fastapi import FastAPI, Query
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import UsernameInvalidError, UsernameNotOccupiedError
import re, os, asyncio

app = FastAPI()

# === 1️⃣ Your Telegram API credentials ===
API_ID = int(os.getenv("API_ID", "1234567"))
API_HASH = os.getenv("API_HASH", "your_api_hash_here")


@app.get("/")
def home():
    return {
        "message": "Username ⇄ ID API by @EskedarEjigu",
        "usage": "/convert?query=@username_or_id"
    }


@app.get("/convert")
async def convert(query: str = Query(..., description="Telegram username or user ID")):
    query = query.strip()

    async def process_query():
        async with TelegramClient(StringSession(), API_ID, API_HASH) as client:
            if query.startswith('@'):
                user = await client.get_entity(query)
                return {"username": query, "id": user.id}

            elif re.fullmatch(r'\d+', query):
                user = await client.get_entity(int(query))
                username = f"@{user.username}" if user.username else None
                return {"id": query, "username": username}

            else:
                return {"error": "Invalid input. Use @username or numeric user ID."}

    try:
        return await process_query()

    except UsernameNotOccupiedError:
        return {"error": "Username not found."}
    except UsernameInvalidError:
        return {"error": "Invalid username."}
    except Exception as e:
        return {"error": str(e)}
