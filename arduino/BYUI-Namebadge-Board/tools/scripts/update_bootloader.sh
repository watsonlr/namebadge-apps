#!/usr/bin/env bash
# update_bootloader.sh
# Copies the latest factory_switch.bin from the BYUI-Namebadge4-OTA IDF build
# into this board package.  Run this after rebuilding the factory loader.
#
# Usage:  ./tools/scripts/update_bootloader.sh [IDF_BUILD_DIR]
#   IDF_BUILD_DIR defaults to the sibling BYUI-Namebadge4-OTA/build/ directory.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
BUILD_DIR="${1:-$(cd "$PACKAGE_DIR/../../../BYUI-Namebadge4-OTA/build" && pwd)}"
SRC="$BUILD_DIR/bootloader/bootloader.bin"
DST="$PACKAGE_DIR/bootloader/factory_switch.bin"

if [[ ! -f "$SRC" ]]; then
    echo "ERROR: bootloader not found at $SRC"
    echo "  Build the factory loader first: idf.py build"
    exit 1
fi

cp "$SRC" "$DST"
echo "Copied: $SRC"
echo "    To: $DST"

SIZE=$(wc -c < "$DST")
echo "  Size: $SIZE bytes"
