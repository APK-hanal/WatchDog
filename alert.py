import cv2
import discord
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
import time

load_dotenv()
RTSP_URL = os.getenv("RTSP_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

# If there is motion
async def send_alert(image_path):
    try:
        channel = client.get_channel(CHANNEL_ID)
        await channel.send("I detect Movement", file=discord.File(image_path))
        os.remove(image_path)
        print(f"Sucessfully sent! check Discord")
    except Exception as e:
        print(f"Error occured!! {e}")

# Motion Dectection
last_alert = 0
cooldown = 300

# Region of Interest (ROI)
ROI_Y1 = 0    
ROI_Y2 = 800  
ROI_X1 = 400  
ROI_X2 = 960 
def detect_motion():
    global last_alert
    time.sleep(5)
    cap = cv2.VideoCapture(RTSP_URL)
    if not cap.isOpened():
        print(f"Error while connecting to Camera")
        return
    prev_frame = None
    while True:
        returnn , frame = cap.read()
        if not returnn:
            print("Error! failed to read frame")
            continue
        # Crop to my hallway only
        roi = frame[ROI_Y1:ROI_Y2, ROI_X1:ROI_X2]
        # Use roi instead of frame for motion detection
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        if prev_frame is None:
            prev_frame = gray
            continue
        diff = cv2.absdiff(prev_frame, gray)
        thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
        motion_score = thresh.sum()
        if motion_score > 100000:
            time.sleep(3)
            current_time = time.time()
            if current_time - last_alert > cooldown:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                image_path = f"alert_{timestamp}.jpg"
                cv2.imwrite(image_path, frame)
                asyncio.run_coroutine_threadsafe(
                    send_alert(image_path),
                    client.loop
                )
                last_alert = current_time
        prev_frame = gray

#what happens when the bot loads
@client.event
async def on_ready():
    print(f"Bot is online as {client.user}")
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, detect_motion)
    
try:
    client.run(BOT_TOKEN)
except Exception as e:
    print(e)    