🐍 Raspberry Pi Zero Snake Game

A simple and colorful Snake Game made for the Raspberry Pi Zero W using the Waveshare 1.44" LCD HAT (128×128 ST7735S).

This project lets you play Snake using the joystick and buttons on the LCD HAT — perfect for a mini handheld game setup.

📌 Hardware Used

Raspberry Pi Zero W (v1.1)

Waveshare 1.44" LCD HAT (ST7735S, 128×128 px)

MicroSD Card (8GB+)

5V Power Supply / Phone Charger

📦 Python Libraries Used

These are the required libraries:

luma.core
luma.lcd
RPi.GPIO
Pillow


These are installed automatically when you run:

pip3 install -r requirements.txt

🚀 Setup Guide (Step-by-Step for Beginners)
1. Update Raspberry Pi
sudo apt-get update
sudo apt-get upgrade -y

2. Enable SPI (Required for Display)
sudo raspi-config


Go to:

Interface Options → SPI → Enable

Reboot if asked.

3. Install Required System Packages
sudo apt-get install python3-pip python3-pil python3-numpy \
libopenjp2-7 libtiff5 libjpeg-dev zlib1g-dev git -y

4. Download This Game

Clone your GitHub repo:

git clone https://github.com/Shrees1ngh/pi-snake-game.git
cd pi-snake-game

5. Install Python Dependencies

Just run:

pip3 install -r requirements.txt


No virtual environment needed — simple setup.

🎮 Controls (LCD HAT Buttons)
Button / Joystick	Action
Joystick Up	Move Up
Joystick Down	Move Down
Joystick Left	Move Left
Joystick Right	Move Right
Joystick Press	Pause / Resume
Key 1	Pause
Key 2	Start / Restart
Key 3	Exit Game
🕹️ Run the Game
python3 snake.py


Game will start immediately on the LCD.

🔧 Auto-Start When Pi Boots (Optional)

If you want the game to run automatically on boot:

sudo nano /etc/rc.local


Add this before exit 0:

/usr/bin/python3 /home/pi/pi-snake-game/snake.py &


Save → Exit → Reboot.

❗ Troubleshooting
Screen is white / black

Make sure SPI is enabled

Make sure display is fully connected

Try restarting the Pi

Error: Module Not Found

Run again:

pip3 install -r requirements.txt

High score not saving

Try:

sudo python3 snake.py

📁 Project Structure
pi-snake-game/
│── snake.py           # Main game file
│── highscore.txt      # Saved automatically
│── requirements.txt   # Python dependencies
│── README.md          # This file

📝 License

Free to use, modify, and improve.
