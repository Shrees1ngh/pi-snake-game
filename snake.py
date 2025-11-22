import time
import random
import threading
import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
from luma.core.interface.serial import spi
from luma.lcd.device import st7735

# ========================
#  LCD SETUP (ROTATE 0)
# ========================
serial = spi(
    port=0,
    device=0,
    gpio_DC=25,
    gpio_RST=27,
    gpio_CS=8
)

device = st7735(
    serial,
    width=128,
    height=128,
    rotate=0,
    invert=False
)

# ========================
#  JOYSTICK + BUTTONS
# ========================
GPIO.setmode(GPIO.BCM)

JOY_UP = 6
JOY_DOWN = 19
JOY_LEFT = 5
JOY_RIGHT = 26
JOY_PRESS = 16    # SAME as KEY3

KEY1 = 21   # Pause
KEY2 = 20   # Restart
KEY3 = 16   # Exit (same pin as joystick press)

pins = [JOY_UP, JOY_DOWN, JOY_LEFT, JOY_RIGHT, JOY_PRESS, KEY1, KEY2, KEY3]
for p in pins:
    GPIO.setup(p, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ========================
#  GAME STATE
# ========================
PIXEL = 8
GRID = 16

def reset_game():
    return {
        "snake": [(5, 5), (4, 5), (3, 5)],
        "direction": "RIGHT",
        "food": (random.randint(0, GRID - 1), random.randint(0, GRID - 1)),
        "game_over": False,
        "score": 0,
        "speed": 0.20,
        "paused": False
    }

state = reset_game()
font = ImageFont.load_default()

# ========================
#  COLOR FUNCTION
# ========================
def rainbow_color(i):
    colors = [
        (255,0,0),(255,128,0),(255,255,0),
        (0,255,0),(0,255,255),(0,128,255),(255,0,255)
    ]
    return colors[i % len(colors)]

# ========================
#  JOYSTICK THREAD
# ========================
def joystick_controls():
    global state
    while True:

        # Movement
        if GPIO.input(JOY_UP) == 0 and state["direction"] != "DOWN":
            state["direction"] = "UP"
        elif GPIO.input(JOY_DOWN) == 0 and state["direction"] != "UP":
            state["direction"] = "DOWN"
        elif GPIO.input(JOY_LEFT) == 0 and state["direction"] != "RIGHT":
            state["direction"] = "LEFT"
        elif GPIO.input(JOY_RIGHT) == 0 and state["direction"] != "LEFT":
            state["direction"] = "RIGHT"

        # ========= FINAL CONTROL MAP ==========
        # KEY1 = Pause
        if GPIO.input(KEY1) == 0:
            state["paused"] = not state["paused"]
            time.sleep(0.3)

        # KEY2 = Restart
        if GPIO.input(KEY2) == 0:
            state = reset_game()
            time.sleep(0.3)

        # KEY3 / Joystick Press = Exit
        if GPIO.input(KEY3) == 0:
            state["game_over"] = True
            break
        # =======================================

        time.sleep(0.05)

threading.Thread(target=joystick_controls, daemon=True).start()

# ========================
#  GAME LOOP
# ========================
while not state["game_over"]:

    if not state["paused"]:
        time.sleep(state["speed"])

        hx, hy = state["snake"][0]

        if state["direction"] == "UP": hy -= 1
        if state["direction"] == "DOWN": hy += 1
        if state["direction"] == "LEFT": hx -= 1
        if state["direction"] == "RIGHT": hx += 1

        hx %= GRID
        hy %= GRID
        new_head = (hx, hy)

        if new_head in state["snake"]:
            state["game_over"] = True
            break

        state["snake"].insert(0, new_head)

        if new_head == state["food"]:
            state["score"] += 1
            state["speed"] = max(0.05, state["speed"] - 0.01)
            state["food"] = (
                random.randint(0, GRID - 1),
                random.randint(0, GRID - 1)
            )
        else:
            state["snake"].pop()

    # Draw frame
    img = Image.new("RGB", (128,128), (0,0,0))
    draw = ImageDraw.Draw(img)

    for i, (x,y) in enumerate(state["snake"]):
        draw.rectangle((x*PIXEL,y*PIXEL,x*PIXEL+PIXEL,y*PIXEL+PIXEL),
                       fill=rainbow_color(i))

    fx, fy = state["food"]
    draw.rectangle((fx*PIXEL, fy*PIXEL, fx*PIXEL+PIXEL, fy*PIXEL+PIXEL),
                   fill=(255,0,0))

    draw.text((2,2), f"Score: {state['score']}", fill=(255,255,0), font=font)

    if state["paused"]:
        draw.text((40,60), "PAUSED", fill=(255,255,255), font=font)

    device.display(img)

# GAME OVER
img = Image.new("RGB",(128,128),(0,0,0))
draw = ImageDraw.Draw(img)
draw.text((20,40),"GAME OVER", fill=(255,0,0), font=font)
draw.text((20,70),f"Score: {state['score']}", fill=(0,255,0), font=font)
device.display(img)

time.sleep(3)
GPIO.cleanup()