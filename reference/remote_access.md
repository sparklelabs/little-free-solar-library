# Guide: Wireless Remote Access (Web Workflow)

This guide describes how to "remote in" to the **Little Free Solar Library** microcontroller wirelessly over its broadcasted Wi-Fi access point. This enables file management, live editing, and REPL console access directly from your web browser without a USB cable.

---

## The Port Conflict & Solution

By default, CircuitPython's built-in Web Workflow runs its management server on **Port 80**. However, the Solar Library captive portal web server (`code.py`) also runs on **Port 80**. 

If both try to bind to Port 80, the board will crash with `OSError: Address already in use`.

**The Solution:** We configure the Web Workflow to run on **Port 8080**, leaving Port 80 dedicated to the public-facing library website.

---

## Step 1: Configuration (`settings.toml`)

Create a file named **`settings.toml`** in the `metro/` folder (so it gets synced to the board root) and add the following lines:

```toml
# Set the password for Web Workflow access (minimum 8 characters)
CIRCUITPY_WEB_API_PASSWORD = "your_secure_password"

# Shift the management server port to avoid captive portal conflicts
CIRCUITPY_WEB_API_PORT = 8080
```

*   Sync the configuration to the board by running `./sync_to_board.sh` (or copying manually).
*   The microcontroller will reboot and start the Web Workflow server in the background.

---

## Step 2: Connecting Wirelessly

Because the Metro is an offline access point, connecting to it will temporarily disconnect your computer from the internet. Follow these steps in order:

1.  **Open the Web App**: While connected to your home internet, open Google Chrome (or a Chromium-based browser) and navigate to the official editor:
    *   **[code.circuitpython.org](https://code.circuitpython.org)**
2.  **Switch Wi-Fi Networks**: Connect your computer to the Metro's broadcasted Wi-Fi: **`Solar_Library_Free`**.
3.  **Initiate Connection**:
    *   In the editor, click **"Connect to Device"** in the top menu.
    *   Select **"Connect over Wi-Fi (Web Workflow)"**.
4.  **Enter Details**:
    *   **Device Address**: `192.168.4.1:8080` (specifying the custom port).
    *   **Password**: Enter the password configured in your `settings.toml`.
5.  **Access the Board**: Click **Connect**.

---

## Features Available Remotely

Once connected, you can:
*   **Wireless File Explorer**: Upload, download, rename, and organize web assets and scripts directly.
*   **Live Web Editor**: Edit and save `code.py` or HTML files directly on the board.
*   **Wireless Serial Console (REPL)**: Monitor print output and debug live python scripts over the air. Press `Ctrl-C` in the terminal pane to access the interactive Python REPL.
