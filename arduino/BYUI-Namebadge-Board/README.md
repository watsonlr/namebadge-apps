# BYUI-Namebadge-Board

Arduino board package for the **BYUI eBadge V4** (ESP32-S3).

Installing this package lets you upload Arduino sketches to the badge safely.
Every upload re-writes the BYUI bootloader and partition table, so the
factory loader (and BOOT-button recovery) is always preserved.

---

## Prerequisites

Install the **ESP32 Arduino core** first (one-time):

1. Open Arduino IDE → **File > Preferences**
2. Add this URL to *Additional boards manager URLs*:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
3. Open **Tools > Board > Boards Manager**, search **esp32**, install
   **esp32 by Espressif Systems** (version 3.x or later)

---

## Install BYUI-Namebadge-Board

### Manual install (recommended for now)

1. Find your Arduino hardware folder:
   - **Linux/Mac:** `~/Arduino/hardware/`
   - **Windows:** `%USERPROFILE%\Documents\Arduino\hardware\`

2. Create the folder `BYUI` inside it if it doesn't exist.

3. Copy the entire `BYUI-Namebadge-Board` folder into it:
   ```
   ~/Arduino/hardware/BYUI/BYUI-Namebadge-Board/
   ```

4. Restart Arduino IDE.

5. Open **Tools > Board** — you should see **BYUI eBadge Boards** with
   **BYUI eBadge V4** listed underneath. Select it.

---

## Upload your first sketch

1. Connect the badge via USB (use a data-capable cable, not charge-only).
2. Select **Tools > Board > BYUI eBadge Boards > BYUI eBadge V4**.
3. Select the correct port under **Tools > Port**.
4. Write or open a sketch, then click **Upload**.

The board package automatically flashes:

| Address  | Binary                    | Purpose                          |
|----------|---------------------------|----------------------------------|
| `0x0000` | `factory_switch.bin`      | BYUI bootloader (always safe)    |
| `0x8000` | partition table           | Badge flash layout               |
| `0xF000` | `ota_data_initial.bin`    | Boot ota_0 on next reset         |
| `0x160000` | your sketch             | Student app slot (ota_0)         |

The factory loader at `0x20000` is **never touched**.

---

## Return to the BYU-I factory loader

At any time:

1. Press **RESET** on the badge.
2. Within ~500 ms, press the **BOOT** button.

The factory loader menu appears.

---

## Package contents

```
BYUI-Namebadge-Board/
├── boards.txt                    ← board hardware settings
├── platform.txt                  ← upload recipe override
├── bootloader/
│   └── factory_switch.bin        ← BYUI custom 2nd-stage bootloader
├── tools/
│   ├── partitions/
│   │   └── byui_badge.csv        ← badge flash partition table
│   └── scripts/
│       ├── generate_ota_data.py  ← regenerates ota_data_initial.bin
│       └── update_bootloader.sh  ← copies new factory_switch.bin from IDF build
└── ota_data/
    └── ota_data_initial.bin      ← pre-built otadata (boot ota_0)
```

---

## Updating the package (maintainers)

When a new factory loader is built and released:

```bash
# From the BYUI-Namebadge-Board directory:
./tools/scripts/update_bootloader.sh          # copies new factory_switch.bin
python3 ./tools/scripts/generate_ota_data.py  # regenerates ota_data_initial.bin
```

Then commit and push to `namebadge-apps`.
