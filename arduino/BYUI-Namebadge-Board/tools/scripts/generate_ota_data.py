#!/usr/bin/env python3
"""
generate_ota_data.py — Generates ota_data_initial.bin for the BYUI eBadge V4.

The file written to flash at 0xF000 (otadata partition, 8 KB) tells the
ESP-IDF bootloader which OTA slot to boot.  This binary sets it to ota_0
(0x160000), so the badge boots the student's sketch after an Arduino Upload.

esp_ota_select_entry_t layout (32 bytes, little-endian):
  offset  0 : ota_seq    uint32  — 1 = ota_0, 2 = ota_1
  offset  4 : seq_label  uint8[20] — unused, all 0xFF
  offset 24 : ota_state  uint32  — 0xFFFFFFFF = ESP_OTA_IMG_VALID
  offset 28 : crc        uint32  — CRC32/ISO-HDLC of bytes 0-27

Two identical 4 KB sectors fill the 8 KB partition.
"""

import struct
import binascii
import os

OUTPUT = os.path.join(os.path.dirname(__file__), '..', '..', 'ota_data', 'ota_data_initial.bin')

def crc32(data: bytes) -> int:
    return binascii.crc32(data) & 0xFFFFFFFF

def make_entry(ota_seq: int) -> bytes:
    seq_label = b'\xFF' * 20
    ota_state = 0xFFFFFFFF          # ESP_OTA_IMG_VALID
    body = struct.pack('<I', ota_seq) + seq_label + struct.pack('<I', ota_state)
    crc = crc32(body)               # CRC32 over first 28 bytes
    return body + struct.pack('<I', crc)  # 32 bytes total

def main():
    entry = make_entry(ota_seq=1)   # 1 → ota_0
    sector = entry + b'\xFF' * (4096 - len(entry))
    ota_data = sector + sector      # two identical 4 KB sectors = 8 KB

    out_path = os.path.normpath(OUTPUT)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'wb') as f:
        f.write(ota_data)
    print(f"Written {len(ota_data)} bytes → {out_path}")

if __name__ == '__main__':
    main()
