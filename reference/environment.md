# Development Environment Workflow

This document records the preferred development environment and workflow for the **Solar Little Library** project. The setup favors a lightweight, terminal-first workflow instead of a heavy IDE like VS Code.

---

## 1. Workspace Layout (Zellij & Helix)
This workflow uses **Zellij** for terminal multiplexing and pane management, and **Helix** as the modal text editor.

### Recommended Zellij Pane Setup
Open a Zellij tab divided into three panes:
1.  **Code Editor Pane:** Runs **Helix** to edit code on the Metro ESP32-S3.
2.  **Serial Log Pane:** Runs **`tio`** to monitor stdout and access the Python REPL.
3.  **Command/Git Pane:** For running tests, managing git, and interacting with the AI agent.

### Code Editing (Helix)
Because the **Adafruit Metro ESP32-S3 N16R8** runs **CircuitPython**, it mounts directly to the host computer as a USB mass storage drive.

*   **Mount Path (macOS):** `/Volumes/CIRCUITPY/`
*   **Main Script:** `/Volumes/CIRCUITPY/code.py`
*   **Workflow:**
    1.  Open `/Volumes/CIRCUITPY/code.py` in **Helix**:
        ```bash
        hx /Volumes/CIRCUITPY/code.py
        ```
    2.  Edit code and save (`:w`).
    3.  CircuitPython automatically detects the write, reloads the environment, and runs the script instantly.

---

## 2. Monitoring & Debugging (Serial Connection)
To view debugging logs (`print` statements) or interact with the CircuitPython Python REPL, use a terminal-based serial viewer.

### Option A: `tio` (Recommended)
`tio` is a simple, lightweight TTY terminal application.
*   **List devices:**
    ```bash
    tio --list
    ```
*   **Connect to Metro ESP32-S3:**
    ```bash
    tio /dev/tty.usbmodem*
    ```

### Option B: `screen`
`screen` is pre-installed on macOS.
*   **Connect to Metro ESP32-S3:**
    ```bash
    screen /dev/tty.usbmodem* 115200
    ```
*   **Disconnect:** Press `Ctrl+A`, then `K`, then `Y` (to kill the session).

---

## 3. Project Management & Task Tracking
*   **BatCave Web UI (port 7673):** Used for Symphony Kanban card tracking and Obsidian knowledge graph exploration.
*   **AI Pair Programmer (Antigravity CLI):** Used for code generation, test script creation, and documentation updates.
