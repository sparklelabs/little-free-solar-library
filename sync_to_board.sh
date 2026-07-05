#!/bin/bash
BOARD_PATH="/Volumes/CIRCUITPY"
SRC_PATH="/Users/arielchuri/Life/projects/personal/solarlibrary/metro"

if [ ! -d "$BOARD_PATH" ]; then
    echo "Error: Metro microcontroller (CIRCUITPY) is not mounted at $BOARD_PATH."
    exit 1
fi

echo "Syncing solarlibrary/metro/ files to Metro ESP32-S3..."
rsync -ruvh --delete "$SRC_PATH/" "$BOARD_PATH/"
echo "✓ Sync complete! Microcontroller will now restart."
