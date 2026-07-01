# Hardware Bill of Materials (BOM)

This document lists the hardware parts selected for the **Solar Little Library** project.

---

## Core Components

| Part Image / Link | Description | Role in Project | Specs |
| :--- | :--- | :--- | :--- |
| Part Image / Link | Description | Role in Project | Specs |
| :--- | :--- | :--- | :--- |
| [Adafruit Metro ESP32-S3](https://www.adafruit.com/product/5500) | Microcontroller board with Wi-Fi/Bluetooth | Main server hosting the offline AP and file directory. | 16 MB Flash, 8 MB PSRAM (N16R8) |
| [Raspberry Pi Pico W](https://www.adafruit.com/product/6315) | Alternative low-cost microcontroller board | Cheaper option with less storage space. | Dual ARM Cortex-M0+ |
| [6V 2W Solar Panel - ETFE [Voltaic P126]](https://www.adafruit.com/product/5366) | High-efficiency solar panel | Harvesting solar energy to power the system off-grid. | 6V, 2W, ETFE coating |
| [Adafruit Universal Solar Charger [bq24074]](https://www.adafruit.com/product/4755) | Solar Lithium Ion/Polymer battery charger | Charging the battery from solar and regulating power. | bq24074 chip, dynamic power path |
| [Lithium Ion Battery - 3.7V 10050mAh](https://www.adafruit.com/product/5035) | High-capacity battery pack | Powering the system overnight and on overcast days. | 3.7V, 10050mAh (10 Ah) |
| [DC Jack Adapter Cable](https://www.adafruit.com/product/2788) | 3.8/1.3mm or 3.5/1.1mm to 5.5/2.1mm adapter | Connecting the solar panel DC output to the charger board. | DC Jack Adapter |

---

## Power Budget Considerations
*   **Solar Panel Output (Peak):** 2W at 6V (~330 mA max).
*   **Metro ESP32-S3 Draw:** ~100 mA to 240 mA when broadcasting Wi-Fi and serving requests.
*   **Battery Backup:** A high-capacity 3.7V 10050mAh Li-Ion battery (Adafruit #5035) will be connected to the bq24074 charger to keep the system running overnight and during overcast days.
