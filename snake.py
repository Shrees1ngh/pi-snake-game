#!/usr/bin/env python3
"""
Snake Game for Raspberry Pi Zero W with Waveshare 1.44" LCD HAT.

Description:
    A classic Snake game implementation specifically designed for the Waveshare 
    1.44-inch LCD HAT (ST7735S driver). It uses the `luma.lcd` library for 
    rendering graphics and `RPi.GPIO` for handling joystick and button inputs.

Hardware Requirements:
    - Raspberry Pi Zero W (v1.1 or newer recommended)
    - Waveshare 1.44inch LCD HAT (128x128 pixel resolution)

Dependencies:
    - luma.lcd
    - luma.core
    - RPi.GPIO
    - Pillow (PIL)

Usage:
    Run the script directly: python3 snake_game.py

Author: [Your Name/Username]
License: MIT (or your preferred license)
"""

import sys
import time
import random
import os
from collections import deque
from PIL import Image, ImageDraw, ImageFont

# Attempt to import GPIO. If running on a non-Pi device (e.g., for testing logic),
# this allows the script to load without crashing, though controls won't work.
try:
    import RPi.GPIO as GPIO
    HAS_GPIO = True
except ImportError:
    HAS_GPIO = False
    print("Warning: RPi.GPIO not found. GPIO features disabled.")

from luma.core.interface.serial import spi
from luma.lcd.device import st7735

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

# SPI Configuration for Waveshare 1.44inch LCD HAT
# These pin numbers (BCM) are specific to the HAT's wiring.
serial = spi(port=0, device=0, gpio_DC=25, gpio_RST=27, gpio_CS=8)

# Screen Device Initialization
# ST7735S controller setup. 
# h_offset and v_offset are often needed to align the image on these small screens.
device = st7735(serial, width=128, height=128, rotate=0, bgr=True, 
                h_offset=0, v_offset=2) 

# Game Constants
SCREEN_W = 128
SCREEN_H = 128
CELL = 8                    # Size of one grid cell in pixels
GRID_W = SCREEN_W // CELL   # Number of columns
GRID_H = SCREEN_H // CELL   # Number of rows

# File path for storing high scores persistently
HIGHSCORE_FILE = os.path.join(os.path.dirname(__file__), "highscore.txt")

# Font for text rendering
FONT = ImageFont.load_default()

# Color Definitions (R, G, B)
CLR_BG = (0, 0, 0)          # Background: Black
CLR_FOOD = (255, 50, 50)    # Food: Red
CLR_TEXT = (255, 255, 255)  # Text: White
CLR_HI = (255, 215, 0)      # High Score: Gold
CLR_HEAD = (0, 100, 0)      # Snake Head: Dark Green

# ---------------------------------------------------------
# GPIO MAPPING
# ---------------------------------------------------------
# BCM pin numbers for the buttons/joystick on the Waveshare HAT
PIN_UP = 6
PIN_DOWN = 19
PIN_LEFT = 5
PIN_RIGHT = 26
PIN_SELECT = 13  # Joystick Press
PIN_KEY1 = 21
PIN_KEY2 = 20
PIN_KEY3 = 16

# ---------------------------------------------------------
# GAME LOGIC
# ---------------------------------------------------------
DIRS = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}
OPPOSITE = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}

class SnakeGame:
    """
    Main Game Class handling state, logic, and rendering.
    """
    def __init__(self):
        self.high_score = self.load_highscore()
        self.exiting = False
        self.state = "MENU" 
        self.reset_game_data()

    def load_highscore(self):
        """Reads the high score from a file, returns 0 if file not found."""
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                return int(f.read())
        except:
            return 0

    def save_highscore(self):
        """Writes the current high score to a file."""
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(self.high_score))

    def reset_game_data(self):
        """Resets the snake, food, score, and speed for a new game."""
        midx, midy = GRID_W // 2, GRID_H // 2
        # Initialize snake in the middle of the screen
        self.snake = deque([(midx, midy), (midx - 1, midy), (midx - 2, midy)])
        self.direction = "RIGHT"
        self.next_direction = "RIGHT"
        self.score = 0
        self.paused = False
        self.base_fps = 5 
        self.fps = self.base_fps
        self.place_food()

    def start_game(self):
        """Transitions state to PLAYING."""
        self.reset_game_data()
        self.state = "PLAYING"

    def place_food(self):
        """Randomly places food on the grid, ensuring it doesn't overlap the snake."""
        snake_set = set(self.snake)
        while True:
            fx, fy = random.randint(0, GRID_W - 1), random.randint(0, GRID_H - 1)
            if (fx, fy) not in snake_set:
                self.food = (fx, fy)
                break

    def change_dir(self, d):
        """
        Updates direction if valid (cannot reverse 180 degrees instantly).
        Buffered into next_direction to prevent suicide on quick key presses.
        """
        if OPPOSITE[d] != self.direction:
            self.next_direction = d

    def update(self):
        """
        Main game loop update: moves snake, checks collisions, handles eating.
        """
        if self.state != "PLAYING" or self.paused: return

        self.direction = self.next_direction
        dx, dy = DIRS[self.direction]
        hx, hy = self.snake[0]

        # Calculate new head position with wrap-around logic
        nx, ny = (hx + dx) % GRID_W, (hy + dy) % GRID_H
        nh = (nx, ny)

        # Collision Check: If new head is inside the snake body
        if nh in self.snake:
            self.state = "GAMEOVER"
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_highscore()
            return

        self.snake.appendleft(nh)

        # Check if food is eaten
        if nh == self.food:
            self.score += 1
            self.place_food()
            # Increase speed as score increases, capped at 25 FPS
            new_fps = self.base_fps + (self.score // 2)
            self.fps = min(new_fps, 25) 
        else:
            # Remove tail if no food eaten
            self.snake.pop()

    def draw(self):
        """
        Renders the current game state to a PIL Image.
        Returns: Image object to be displayed on LCD.
        """
        img = Image.new("RGB", (128, 128), CLR_BG)
        d = ImageDraw.Draw(img)

        # --- 1. EXIT SCREEN ---
        if self.exiting:
            d.rectangle([0,0,128,128], fill=(0,0,0))
            self._draw_centered(d, "GOODBYE!", -10, (0, 255, 0))
            self._draw_centered(d, "Exiting...", 10, (150,150,150))
            return img

        # --- 2. MENU SCREEN ---
        if self.state == "MENU":
            d.rectangle([10, 10, 118, 118], outline=(0, 200, 0))
            self._draw_centered(d, "SNAKE", -20, (0, 255, 0))
            self._draw_centered(d, "GAME", -8, (0, 200, 0))
            self._draw_centered(d, "Press Key 2", 15, CLR_TEXT)
            self._draw_centered(d, "to Start", 27, CLR_TEXT)
            return img

        # --- 3. GAMEPLAY RENDER ---
        
        # Draw Food
        fx, fy = self.food
        d.ellipse([fx*CELL, fy*CELL, fx*CELL+CELL-1, fy*CELL+CELL-1], fill=CLR_FOOD)

        # Draw Snake
        for i, (x, y) in enumerate(self.snake):
            rect = [x*CELL, y*CELL, x*CELL+CELL-1, y*CELL+CELL-1]
            
            if i == 0:
                # HEAD: Solid Dark Green
                d.rectangle(rect, fill=CLR_HEAD)
            else:
                # BODY: Gradient Green (Bright -> Dark towards tail)
                fade = max(50, 255 - (i * 8)) 
                body_color = (0, fade, 0)
                d.rectangle(rect, fill=body_color)

        # --- 4. UI OVERLAY ---
        if self.state == "GAMEOVER":
            d.rectangle([10, 30, 118, 100], fill=(0,0,0), outline=(255,255,255))
            self._draw_centered(d, "GAME OVER", -15, CLR_FOOD)
            self._draw_centered(d, f"SCORE: {self.score}", 0, CLR_TEXT)
            self._draw_centered(d, f"HIGH: {self.high_score}", 10, CLR_HI)
            self._draw_centered(d, "[Key 2 to Retry]", 25, (100,100,100))
            
        elif self.paused:
             self._draw_centered(d, "PAUSED", 0, CLR_TEXT)
        else:
            # HUD: Current Score and High Score
            d.text((1, 0), f"S:{self.score}", fill=CLR_TEXT, font=FONT)
            d.text((90, 0), f"HI:{self.high_score}", fill=CLR_HI, font=FONT)

        return img

    def _draw_centered(self, d, txt, y_off, clr):
        """Helper to draw centered text on the screen."""
        bbox = d.textbbox((0, 0), txt, font=FONT)
        w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
        d.text(((128 - w) // 2, (128 - h) // 2 + y_off), txt, fill=clr, font=FONT)

# ---------------------------------------------------------
# HARDWARE INPUT SETUP
# ---------------------------------------------------------
def gpio_setup():
    """Initializes GPIO pins with internal Pull-Up resistors."""
    if not HAS_GPIO: return False
    GPIO.setmode(GPIO.BCM)
    for p in [PIN_UP, PIN_DOWN, PIN_LEFT, PIN_RIGHT, PIN_SELECT, PIN_KEY1, PIN_KEY2, PIN_KEY3]:
        GPIO.setup(p, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    return True

def read_input():
    """Reads GPIO states and returns a command string (UP, DOWN, EXIT, etc)."""
    if not HAS_GPIO: return None
    # Input is active LOW (0 means pressed)
    if GPIO.input(PIN_UP) == 0: return "UP"
    if GPIO.input(PIN_DOWN) == 0: return "DOWN"
    if GPIO.input(PIN_LEFT) == 0: return "LEFT"
    if GPIO.input(PIN_RIGHT) == 0: return "RIGHT"
    if GPIO.input(PIN_SELECT) == 0: return "PAUSE"
    if GPIO.input(PIN_KEY1) == 0: return "PAUSE"
    if GPIO.input(PIN_KEY2) == 0: return "RESTART" 
    if GPIO.input(PIN_KEY3) == 0: return "EXIT"
    return None

# ---------------------------------------------------------
# MAIN EXECUTION
# ---------------------------------------------------------
def main():
    gpio_ok = gpio_setup()
    game = SnakeGame()
    last_update = time.time()

    print("Snake Game Started. Press Key 3 to Exit.")

    try:
        while True:
            # 1. Handle Input
            if gpio_ok:
                sig = read_input()
                if sig:
                    if sig == "EXIT":
                        game.exiting = True
                        device.display(game.draw())
                        time.sleep(2) 
                        break
                    
                    elif sig == "RESTART":
                        if game.state == "MENU" or game.state == "GAMEOVER":
                            game.start_game()
                        else:
                            game.reset_game_data()
                            game.state = "PLAYING"
                    
                    elif sig == "PAUSE": 
                        if game.state == "PLAYING":
                            game.paused = not game.paused; time.sleep(0.2)
                            
                    elif sig in DIRS and game.state == "PLAYING": 
                        game.change_dir(sig)

            # 2. Update Game Loop
            now = time.time()
            if not game.exiting:
                # Dynamic FPS control: faster updates for PLAYING, slower for MENU
                update_interval = 1.0 / game.fps if game.state == "PLAYING" else 0.1
                
                if (now - last_update >= update_interval):
                    game.update()
                    last_update = now
                    device.display(game.draw())
            
            # 3. Small sleep to prevent 100% CPU usage
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\nUser interrupted via Keyboard.")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        # Cleanup hardware resources
        print("Cleaning up...")
        device.clear()
        if HAS_GPIO: GPIO.cleanup()

if __name__ == "__main__":
    main()
