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

### Via Boards Manager (recommended)

1. Open Arduino IDE → **File > Preferences**
   (Mac: **Arduino IDE > Settings**).

2. Add this URL to **"Additional boards manager URLs"**:
   ```
   https://raw.githubusercontent.com/watsonlr/namebadge-apps/main/arduino/BYUI-Namebadge-Board/package_byui_index.json
   ```

3. Open **Tools > Board > Boards Manager**, search `BYUI`, and
   click **Install** next to **BYUI eBadge Boards**.

4. Select **Tools > Board > BYUI eBadge Boards > BYUI eBadge V4**.

### Manual install (advanced)

Clone `namebadge-apps` and copy the folder directly:

```bash
# Linux / Mac
mkdir -p ~/Arduino/hardware/BYUI
cp -r namebadge-apps/arduino/BYUI-Namebadge-Board ~/Arduino/hardware/BYUI/
```

Restart Arduino IDE, then select **Tools > Board > BYUI eBadge Boards > BYUI eBadge V4**.

---

## Upload your first sketch

1. Connect the badge via USB (use a data-capable cable, not charge-only).
2. Select **Tools > Board > BYUI eBadge Boards > BYUI eBadge V4**.
3. Select the correct port under **Tools > Port**.
4. Write or open a sketch, then click **Upload**.

The board package automatically flashes:

| Address    | Binary                 | Purpose                       |
|------------|------------------------|-------------------------------|
| `0x000000` | `factory_switch.bin`   | BYUI bootloader (always safe) |
| `0x008000` | partition table        | Badge flash layout            |
| `0x00F000` | `ota_data_initial.bin` | Boot ota_0 on next reset      |
| `0x160000` | your sketch            | Student app slot (ota_0)      |

The factory loader at `0x20000` is **never touched**.

See [GETTING_STARTED.md](GETTING_STARTED.md) for a full step-by-step guide
including a working Blink sketch.

---

## Return to the BYU-I factory loader

At any time:

1. Press **RESET** on the badge.
2. Within ~500 ms, press the **BOOT** button.

The factory loader menu appears. Press **RESET** again (without BOOT) to
return to your sketch.

---

## Package contents

```
BYUI-Namebadge-Board/
├── boards.txt                    ← board hardware settings
├── platform.txt                  ← upload recipe + partition prebuild hook
├── GETTING_STARTED.md            ← student step-by-step guide
├── README.md                     ← this file
├── bootloader/
│   └── factory_switch.bin        ← BYUI custom 2nd-stage bootloader
├── ota_data/
│   └── ota_data_initial.bin      ← pre-built otadata (boots ota_0)
└── tools/
    ├── copy_partitions.py        ← prebuild helper (copies CSV to build path)
    ├── partitions/
    │   └── byui_badge.csv        ← badge flash partition table
    └── scripts/
        ├── generate_ota_data.py  ← regenerates ota_data_initial.bin
        └── update_bootloader.sh  ← copies new factory_switch.bin from IDF build
```

---

## Releasing a new version (maintainers)

1. Bump `version=` in `platform.txt` (e.g. `1.0.1`).

2. Update binaries if needed:
   ```bash
   # From the BYUI-Namebadge-Board directory:
   ./tools/scripts/update_bootloader.sh          # copies new factory_switch.bin
   python3 ./tools/scripts/generate_ota_data.py  # regenerates ota_data_initial.bin
   ```

3. Build the versioned zip (from `namebadge-apps/arduino/`):
   ```bash
   cd namebadge-apps/arduino
   zip -r BYUI-Namebadge-Board-1.0.1.zip BYUI-Namebadge-Board \
       --exclude "*.git*" --exclude "*/.DS_Store" --exclude "*/package_byui_index.json"
   sha256sum BYUI-Namebadge-Board-1.0.1.zip
   wc -c < BYUI-Namebadge-Board-1.0.1.zip
   ```

4. **Append** a new entry to the `platforms` array in `package_byui_index.json`
   (do not replace the old entry — Boards Manager needs full history for upgrades).
   Update `url`, `archiveFileName`, `checksum`, `size`, and `version`.

5. Commit and push:
   ```bash
   git add BYUI-Namebadge-Board/ BYUI-Namebadge-Board-1.0.1.zip
   git commit -m "Release BYUI-Namebadge-Board v1.0.1"
   git push
   ```

6. Create a GitHub Release tagged `arduino-v1.0.1` and upload
   `BYUI-Namebadge-Board-1.0.1.zip` as the release asset.
