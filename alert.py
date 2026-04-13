import cv2
import discord
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
import pygame

load_dotenv()
RTSP_URL = os.getenv("RTSP_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

# If there is motion
async def send_alert(image_path):
    channel = client.get_channel(CHANNEL_ID)
    await channel.send("Something movedddd", file=discord.File(image_path))
    os.remove(image_path)

# Motion Dectection
def detect_motion():
    cap = cv2.VideoCapture(RTSP_URL)
    prev_frame = None
    while True:
        returnn , frame = cap.read()
        if not returnn:
            print("Error! failed to read frame")
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        if prev_frame is None:
            prev_frame = gray
            continue
        diff = cv2.absdiff(prev_frame, gray)
        thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
        motion_score = thresh.sum()
        if motion_score > 100000:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = f"alert_{timestamp}.jpg"
            cv2.imwrite(image_path, frame)
            asyncio.run_coroutine_threadsafe(
                send_alert(image_path),
                client.loop
            )
        prev_frame = gray


# Temporary Visualization
pygame.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("WatchDog Visualizer")

clock = pygame.time.Clock()
cap = cv2.VideoCapture(RTSP_URL)
running = True
prev_frame = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    
    screen.fill((0, 0, 0))
    ret, frame = cap.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if prev_frame is not None:
            diff = cv2.absdiff(prev_frame, gray)
            thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
            motion_score = thresh.sum()

            # Convert all frames for pygame
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_rgb = cv2.resize(frame_rgb, (400, 300))

            diff_color = cv2.cvtColor(diff, cv2.COLOR_GRAY2RGB)
            diff_color = cv2.resize(diff_color, (400, 300))

            thresh_color = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)
            thresh_color = cv2.resize(thresh_color, (400, 300))

            # Draw all three on screen
            screen.blit(pygame.surfarray.make_surface(frame_rgb.swapaxes(0,1)), (0, 0))
            screen.blit(pygame.surfarray.make_surface(diff_color.swapaxes(0,1)), (400, 0))
            screen.blit(pygame.surfarray.make_surface(thresh_color.swapaxes(0,1)), (0, 300))
            if motion_score != 0 and motion_score >= 30000:
                print(motion_score)
            # Display motion score as text
            font = pygame.font.SysFont("monospace", 20)
            score_text = font.render(f"Motion score: {int(motion_score)}", True, (255, 255, 255))
            screen.blit(score_text, (400, 300))

        prev_frame = gray
    pygame.display.flip()
    clock.tick(30)
pygame.quit()
        