# Raspberry Pi Zero Snake Game

A simple and colorful Snake game made for the Raspberry Pi Zero W using the Waveshare 1.44" LCD HAT (128×128, ST7735S).

This project lets you play Snake using the joystick and buttons on the LCD HAT — perfect for a mini handheld game setup.

---

## Hardware Used

- Raspberry Pi Zero W (v1.1)
- Waveshare 1.44" LCD HAT (ST7735S, 128×128 px)
- MicroSD Card (8GB+)
- 5V Power Supply / Phone Charger

---

## Python Libraries Used

These are the required libraries:

luma.core
luma.lcd
RPi.GPIO
Pillow

cpp
Copy code

Install them using:

pip3 install -r requirements.txt

yaml
Copy code

---

## Setup Guide (Beginner Friendly)

### 1. Update Raspberry Pi

sudo apt-get update
sudo apt-get upgrade -y

yaml
Copy code

---

### 2. Enable SPI (Required for Display)

sudo raspi-config

yaml
Copy code

Go to:

**Interface Options → SPI → Enable**

Reboot if required.

---

### 3. Install System Dependencies

sudo apt-get install python3-pip python3-pil python3-numpy
libopenjp2-7 libtiff5 libjpeg-dev zlib1g-dev git -y

yaml
Copy code

---

### 4. Download This Repository

git clone https://github.com/Shrees1ngh/pi-snake-game.git
cd pi-snake-game

yaml
Copy code

---

### 5. Install Python Dependencies

pip3 install -r requirements.txt

yaml
Copy code

---

## Controls

| Button / Joystick | Action |
|-------------------|--------|
| Joystick Up | Move Up |
| Joystick Down | Move Down |
| Joystick Left | Move Left |
| Joystick Right | Move Right |
| Joystick Press | Pause / Resume |
| Key 1 | Pause |
| Key 2 | Start / Restart |
| Key 3 | Exit Game |

---

## Run the Game

python3 snake.py

yaml
Copy code

---

## Auto-Start on Boot (Optional)

If you want the game to start automatically on boot:

sudo nano /etc/rc.local

javascript
Copy code

Add this above `exit 0`:

/usr/bin/python3 /home/pi/pi-snake-game/snake.py &

yaml
Copy code

Save and reboot.

---

## Troubleshooting

### Screen stays white / black
- SPI not enabled  
- Display not connected properly  
- Restart Raspberry Pi  

### ModuleNotFoundError
Run:

pip3 install -r requirements.txt

python
Copy code

### High score not saving
Run once with:

sudo python3 snake.py

yaml
Copy code

---

## Project Structure

pi-snake-game/
│── snake.py
│── highscore.txt
│── requirements.txt
│── README.md

yaml
Copy code

---

## License

Free to use and modify.
