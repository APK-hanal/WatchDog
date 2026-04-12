import cv2
import discord
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

RTSP_URL = os.getenv("RTSP_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def send_alert(image_path):
    channel = client.get_channel(CHANNEL_ID)
    await channel.send("Motion detected!", file=discord.File(image_path))
    os.remove(image_path)
    