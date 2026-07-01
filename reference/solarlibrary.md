# Solar Little Library Configuration (Adafruit Metro ESP32-S3 N16R8)

This guide documents the software setup, configuration, and code implementation for running the **Solar Little Library** offline server on the **Adafruit Metro ESP32-S3 N16R8** microcontroller.

---

## 1. Hardware Overview: Metro ESP32-S3 N16R8
The core server runs on the Adafruit Metro ESP32-S3 (N16R8 variant), which features:
*   **Processor:** Dual-core Xtensa LX7 running at 240MHz.
*   **Storage & Memory:** 16 MB Flash (N16) and 8 MB External PSRAM (R8).
*   **Connectivity:** Integrated 2.4 GHz Wi-Fi and Bluetooth 5 (LE).
*   **Built-in Storage Expansion:** MicroSD card slot on the underside of the board, which allows the offline library to host gigabytes of PDFs, EPUBs, and media files.
*   **Form Factor:** Arduino Uno-compatible footprint with built-in STEMMA QT connector, NeoPixel, and USB-C.

---

## 2. Setting Up CircuitPython

To flash CircuitPython onto the Metro ESP32-S3 N16R8:

1.  **Download the Firmware:**
    Get the latest stable UF2 bootloader file for the **Adafruit Metro ESP32-S3** from the [CircuitPython Downloads page](https://circuitpython.org/board/adafruit_metro_esp32s3_n16r8/).
2.  **Enter Bootloader Mode:**
    *   Connect the board to your computer using a USB-C cable.
    *   Double-click the **Reset** button on the Metro ESP32-S3. The onboard NeoPixel LED should pulse green, indicating that it is in bootloader mode.
    *   A new drive named `METROS3BOOT` will appear on your computer.
3.  **Flash the Board:**
    *   Drag and drop the downloaded `.uf2` file onto the `METROS3BOOT` drive.
    *   The board will reboot automatically, and a new USB drive named `CIRCUITPY` will mount.

---

## 3. Libraries & Dependencies

You need to copy required libraries from the [Adafruit CircuitPython Library Bundle](https://circuitpython.org/libraries) matching your major CircuitPython version.

Create a `lib/` directory inside your `CIRCUITPY` drive and copy the following files/folders:
1.  **`adafruit_httpserver/`** (folder) — Used for setting up the web server and handling HTTP requests.
2.  **`adafruit_requests.mpy`** (file) — Used for making outgoing HTTP requests if the board connects to an external network.

---

## 4. Serving Files from the Built-in MicroSD Card

Because the Metro ESP32-S3 N16R8 has a built-in microSD slot on the back, we can serve large e-books and documentation directly from it. 

### MicroSD Pins on Metro ESP32-S3:
*   **CS (Chip Select):** `board.SD_CS`
*   **SPI Bus:** Standard SPI (`board.MOSI`, `board.MISO`, `board.SCK`)

### Mounting the SD Card in CircuitPython:
Using the built-in C-optimized `sdcardio` module:
```python
import board
import busio
import sdcardio
import storage

# Initialize SPI and mount SD card
spi = board.SPI()
sd_cs = board.SD_CS
sdcard = sdcardio.SDCard(spi, sd_cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

print("SD Card successfully mounted at /sd")
```

---

## 5. Web Server & Captive Portal Code (`code.py`)

The main script runs a Wi-Fi Access Point, a non-blocking web server using `adafruit_httpserver`, and a custom UDP DNS redirector on Port 53 to spoof all DNS requests to redirect users to the landing page.

Copy the codebase at [code.py](file:///Users/arielchuri/Life/projects/personal/solarlibrary/code.py) directly into the root of the `CIRCUITPY` drive.

### Quick Verification using Helix & `tio`:
1.  Open the file inside your terminal workflow:
    ```bash
    hx /Volumes/CIRCUITPY/code.py
    ```
2.  Connect to the serial console to view logs:
    ```bash
    tio /dev/tty.usbmodem*
    ```
3.  Save files in Helix (`:w`) to trigger automatic reloads and verify connection logs in the `tio` pane.
