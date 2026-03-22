# Getting Started — BYUI eBadge V4 with Arduino

This guide walks you through writing your very first program for the
BYUI eBadge V4 using the Arduino IDE.  By the end you will have an LED
blinking on your badge.

---

## What you need

| Item | Notes |
|------|-------|
| BYUI eBadge V4 | Must have WiFi configured (factory setup complete) |
| USB cable | **Data-capable** — charge-only cables will not work |
| PC / Mac / Linux computer | Windows 10+, macOS 11+, or Ubuntu 22+ |
| Arduino IDE 2.x | Free download at arduino.cc/en/software |

---

## Step 1 — Install Arduino IDE

Download and install **Arduino IDE 2** from:
```
https://www.arduino.cc/en/software
```
Choose the installer for your operating system and run it.

---

## Step 2 — Add the ESP32 board support

The BYUI badge uses an ESP32-S3 chip.  Arduino IDE needs the ESP32
board package to know how to compile for it.

1. Open Arduino IDE.
2. Go to **File > Preferences** (Mac: **Arduino IDE > Settings**).
3. Find the field **"Additional boards manager URLs"** and paste in:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
4. Click **OK**.
5. Go to **Tools > Board > Boards Manager**.
6. In the search box type `esp32`.
7. Find **"esp32 by Espressif Systems"** and click **Install**.
   (This downloads ~250 MB — give it a few minutes.)

---

## Step 3 — Install the BYUI board package

The BYUI board package tells Arduino exactly how to upload safely to
your badge without overwriting the built-in recovery menu.

1. Download or clone `namebadge-apps` from GitHub:
   ```
   https://github.com/watsonlr/namebadge-apps
   ```
2. Find your Arduino **hardware** folder:
   - **Windows:** `C:\Users\<YourName>\Documents\Arduino\hardware\`
   - **Mac:**     `~/Documents/Arduino/hardware/`
   - **Linux:**   `~/Arduino/hardware/`
3. Inside the `hardware` folder, create a new folder called `BYUI`
   (if it does not already exist).
4. Copy the entire `arduino/BYUI-Namebadge-Board` folder into `BYUI`:
   ```
   hardware/
   └── BYUI/
       └── BYUI-Namebadge-Board/   ← paste it here
               boards.txt
               platform.txt
               bootloader/ ...
               ...
   ```
5. **Restart Arduino IDE completely** (close and reopen).
6. Go to **Tools > Board** — you should now see
   **BYUI eBadge Boards** in the list.
7. Select **BYUI eBadge V4**.

---

## Step 4 — Connect your badge

1. Plug your badge into your computer with the USB cable using the
   connector labeled **J1** (the one near the CP2102 chip).
2. In Arduino IDE go to **Tools > Port** and select the port that
   appeared when you plugged in the badge.
   - Windows: it will look like `COM3` or `COM7`
   - Mac/Linux: it will look like `/dev/ttyUSB0` or `/dev/cu.usbserial-...`

> **Tip:** If no new port appears, your cable is charge-only.
> Try a different cable.

---

## Step 5 — Write the Blink sketch

1. In Arduino IDE go to **File > New Sketch**.
2. Delete everything in the editor and type (or paste) this:

```cpp
// BYUI eBadge V4 — Blink
// Blinks the single-color LED on GPIO 6.

#define LED_PIN 6

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_PIN, HIGH);   // turn LED on
  delay(500);                    // wait half a second
  digitalWrite(LED_PIN, LOW);    // turn LED off
  delay(500);                    // wait half a second
}
```

---

## Step 6 — Upload

Click the **Upload** button (the right-arrow icon, or press Ctrl+U).

Arduino IDE will:
1. Compile your sketch (takes 10–30 seconds the first time)
2. Connect to the badge
3. Flash the sketch

You will see a progress bar in the output panel.  When it finishes you
should see:

```
Hard resetting via RTS pin...
Done
```

The badge will reset automatically and your LED will start blinking.

---

## What just happened?

Every time you click Upload, the BYUI board package writes four things
to the badge:

| Address  | What                       |
|----------|----------------------------|
| `0x0000` | BYUI recovery bootloader   |
| `0x8000` | Badge partition table      |
| `0xF000` | "Boot my sketch" marker    |
| `0x160000` | Your sketch              |

The factory loader (the BYU-I Loader menu) lives at `0x20000` and is
**never touched**, so you can always return to it.

---

## Returning to the BYU-I Loader

At any time:

1. Press the **RESET** button on the badge.
2. Within about half a second, press the **BOOT** button.

The BYU-I Loader menu will appear on the display.

To go back to your sketch, just press **RESET** again without pressing
BOOT.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| **"Board BYUI eBadge V4 not found"** | Make sure the folder is in `hardware/BYUI/BYUI-Namebadge-Board/` and you restarted Arduino IDE |
| **No port shows up** | Try a different USB cable; use the J1 connector |
| **Upload fails / timeout** | Try uploading again; if it keeps failing, manually enter download mode (see below) |
| **LED does not blink after upload** | Check the LED_PIN number matches the LED you are looking at (see pin table below) |
| **Badge shows BYU-I Loader after upload** | Press RESET without holding BOOT — your sketch will run |

### Manual download mode

If the auto-upload keeps timing out:

1. Hold the **BOOT** button on the badge.
2. While holding BOOT, press and release **RESET**.
3. Release BOOT.
4. Immediately click **Upload** in Arduino IDE.

The badge is now waiting for the upload.

---

## Badge LED pin reference

| LED | GPIO | Notes |
|-----|------|-------|
| Single color LED | `6` | Best for simple blink |
| RGB — Red | `2` | |
| RGB — Green | `4` | |
| RGB — Blue | `5` | |
| Addressable strip | `7` | Needs FastLED or NeoPixel library |

---

## Next steps

Try changing the `delay(500)` values to make the LED blink faster or
slower.  Then try blinking the RGB LED by replacing `LED_PIN` with `2`,
`4`, or `5` and running the same sketch three times with different pins.

When you are ready for more, explore the badge hardware:

- **Display** (ILI9341, SPI2) — use the Adafruit ILI9341 library
- **Buttons** — read GPIO 33 (B), 34 (A), 11 (Up), 47 (Down), 21 (Left), 10 (Right)
- **Accelerometer** (MMA8452Q, I2C at 0x1C) — use any MMA8452 Arduino library
- **Buzzer** — PWM tone on GPIO 48
- **Addressable LEDs** — FastLED or Adafruit NeoPixel on GPIO 7
