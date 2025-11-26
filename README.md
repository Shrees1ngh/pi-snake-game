Python Snake for Raspberry Pi Zero W (Waveshare LCD HAT)
========================================================

A classic Snake game written in Python, designed specifically for the **Raspberry Pi Zero W** paired with the **Waveshare 1.44inch LCD HAT** (ST7735S Driver).

This project uses the `luma.lcd` library for rendering and `RPi.GPIO` for the HAT's joystick and button inputs.

Game Screenshots
----------------
![IMG_20251126_092654315_HDR_AE~2](https://github.com/user-attachments/assets/32b64dbf-21c6-4b3c-9869-b4aff18ad3ae)


Hardware Requirements
---------------------

1.  **Raspberry Pi Zero W** (v1.1 or similar).
![IMG_20251126_090319991_HDR_AE](https://github.com/user-attachments/assets/39898ded-6426-4c4c-96c6-39cce3d04d14)
![IMG_20251126_090239718_HDR_AE](https://github.com/user-attachments/assets/7aea283f-b9d8-4fba-84a3-5e95fa49a048)

3.  **Waveshare 1.44inch LCD HAT** (128x128 pixel resolution).
![IMG_20251126_090522471_HDR_AE](https://github.com/user-attachments/assets/23b4d88e-3e60-465f-b748-aea6b8450f59)
![IMG_20251126_090609639_HDR_AE](https://github.com/user-attachments/assets/911fb1c0-acea-4053-85ec-f4ed92031451)

5.  MicroSD Card (8GB+).

6.  Power supply (Micro USB).

🛠️ Complete Setup Guide (From Scratch)
---------------------------------------

If you have a brand new Raspberry Pi Zero W, follow this guide to set it up "headless" (without a monitor/keyboard attached).

### Phase 1: Flashing the OS

You will need a computer (Windows/Mac/Linux) with an SD card reader.

1.  Download and install [**Raspberry Pi Imager**](https://www.raspberrypi.com/software/ "null").

2.  Insert your MicroSD card into your computer.

3.  Open Raspberry Pi Imager.

4.  **Choose OS:** Select `Raspberry Pi OS (other)` -> `Raspberry Pi OS Lite (32-bit)`.

    -   *Note: The "Lite" version is best for this game as it uses less memory and boots faster.*

5.  **Choose Storage:** Select your SD card.

6.  **⚙️ IMPORTANT: Configure Settings (The Gear Icon)** Click the gear icon (bottom right) to open Advanced Options. Set these up now so you don't need a monitor later:

    -   **Set Hostname:** e.g., `snake-pi`.

    -   **Enable SSH:** Check this box. Select "Use password authentication".

    -   **Set username and password:** Create a user (e.g., User: `pi`, Pass: `raspberry`).

    -   **Configure Wireless LAN:** Enter your Wi-Fi Name (SSID) and Password. Select your country code.

7.  Click **Save**, then click **Write**.

8.  Wait for the verification to finish, then remove the SD card.

### Phase 2: Connecting via SSH

1.  Insert the SD card into your Raspberry Pi Zero W.

2.  Attach the **Waveshare LCD HAT** to the GPIO header.

3.  Plug in the power cable. Wait about 2-3 minutes for the first boot.

4.  Open **Command Prompt** (Windows), **PowerShell**, or **Terminal** (Mac/Linux) on your computer.

5.  Type the following command (replace `pi` and `snake-pi` with the username/hostname you set in Phase 1):

    ```
    ssh pi@snake-pi.local

    ```

    -   *If you didn't set a hostname, try `ssh pi@raspberrypi.local`.*

    -   *If that doesn't work, check your router to find the Pi's IP address (e.g., 192.168.1.50) and run `ssh pi@192.168.1.50`.*

6.  Type `yes` when asked to continue connecting.

7.  Enter the password you created. You are now controlling your Pi remotely!

### Phase 3: Enable Screen Hardware (SPI)

Once logged in via SSH, run:

```
sudo raspi-config

```

1.  Navigate to **Interface Options**.

2.  Select **SPI**.

3.  Select **Yes** to enable the SPI interface.

4.  Select **Finish** and ask it to **Reboot**.

5.  Wait 1 minute, then SSH back in (`ssh pi@snake-pi.local`).

### Phase 4: Install Dependencies

The screen drivers require specific system libraries. Copy and paste this command:

```
sudo apt-get update
sudo apt-get install python3-dev python3-pip python3-pil libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjp2-7 libtiff5 git -y

```

### Phase 5: Install and Run the Game

1.  **Clone the repository:**

    ```
    git clone [https://github.com/Shrees1ngh/pi-snake-game.git](https://github.com/Shrees1ngh/pi-snake-game.git)
    cd pi-snake-game

    ```

2.  **Install Python requirements:**

    ```
    pip3 install -r requirements.txt

    ```

3.  **Run the game:**

    ```
    python3 snake_game.py

    ```

🎮 How to Play
--------------
### Project Structure

pi-snake-game/

│── snake.py           # Main game script

│── highscore.txt      # Auto-created

│── requirements.txt   # Python dependencies

│── README.md          # Documentation

### Controls (Waveshare HAT)

| **Button**         | **Action**               |
| ------------------ | ------------------------ |
| **Joystick Up**    | Move Up                  |
| **Joystick Down**  | Move Down                |
| **Joystick Left**  | Move Left                |
| **Joystick Right** | Move Right               |
| **Joystick Press** | Pause Game               |
| **Key 1**          | Pause Game               |
| **Key 2**          | **Start Game / Restart** |
| **Key 3**          | Exit to Terminal         |


### Game Features

-   **High Score:** Automatically saves your best score to `highscore.txt`.

-   **Speed Ramp:** The snake gets faster as you eat more food.

-   **Colors:** Dark Green head, gradient body, red food.

🔧 Troubleshooting
------------------

-   **"Host not found" when SSHing?** Ensure your computer and the Pi are on the exact same Wi-Fi network. If `snake-pi.local` fails, you must find the IP address of the Pi using your router's admin page or a phone app like "Fing".

-   **Screen is black?** Make sure you enabled SPI in `sudo raspi-config`.

-   **Colors look inverted?** Open `snake_game.py` and change `bgr=True` to `bgr=False` in the `device = st7735(...)` line.

-   **Screen has static on edges?** Adjust `v_offset` or `h_offset` in the `st7735` initialization in the code (currently set to `v_offset=2`).

License
-------

Open Source. Feel free to modify and improve!
