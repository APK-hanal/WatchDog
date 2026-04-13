Watch Dog

# Context
My house has security cameras and when i was thinking of something to do with them, i figured I'd try to learn computer Vision and create a notification sender for when someone enters my house.
I picked Discord  as the medium of the notification.

# What it does
It takes note of the region of interest for any motion and when it detects large motion as that of a human or sum similar, it sends a message via the discord bot WatchDog to #alerts channel along with a picture of the motion.

# Limitations
Well, it doesnt detect humans exactly for one as motion is the only factor for the notification to be sent. It is also tailored for my house so it might not work on yours just saying.

# Run locally 

git clone https://github.com/APK-hanal/WatchDog
cd WatchDog
pip install -r requirements.txt
(create a .env file)
python alert.py

# Built with :
Python specifically cv2, discord.py,

By : Apil (APK-hanal)