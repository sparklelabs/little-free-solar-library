# Project Log: Little Free Solar Library

## 2026-07-05: TalentCell Battery Compatibility & System Architecture Review

We reviewed the feasibility of using the **TalentCell Lithium-Ion Battery (Model: YB1203000-USB)** with the currently planned hardware components:
*   **Microcontroller**: Adafruit Metro ESP32-S3
*   **Solar Panel**: 6V 2W Voltaic P126
*   **Charge Controller**: Adafruit Universal Solar Charger (bq24074)

---

### Component Specifications

| Component | Key Specs |
| :--- | :--- |
| **TalentCell YB1203000-USB** | 3S Li-Ion Pack. Nominal: 11.1V. Capacity: 3Ah (33.3 Wh). Max charge voltage: 12.6V. Outputs: DC 9V–12.6V (3A max), USB 5V/2A. Built-in BMS. |
| **Voltaic P126 Solar Panel** | 6V peak voltage ($V_{mp}$), 7V open-circuit voltage ($V_{oc}$), 2W peak output (~330mA). |
| **Adafruit Charger (bq24074)**| 1S Li-Ion charger. Input: 4.75V–10V. Charging output: **4.2V max** (for 3.7V nominal cells). |
| **Adafruit Metro ESP32-S3** | Power options: 5V via USB-C, 7V–9V recommended via DC Barrel Jack (12V absolute max). |

---

### Compatibility Analysis

#### 1. Battery ↔ Charge Controller (Adafruit bq24074)
> [!CAUTION]
> **CRITICAL VOLTAGE MISMATCH**
> The Adafruit bq24074 is a **1S (3.7V/4.2V)** battery charger. It cannot charge a **3S (11.1V/12.6V)** TalentCell battery pack. 
> * The bq24074 outputs a maximum of 4.2V to charge batteries.
> * Connecting the 12.6V TalentCell to the battery terminal of the bq24074 could trigger safety cut-offs or damage the controller.

#### 2. Battery ↔ Solar Panel (6V 2W)
> [!WARNING]
> **INSUFFICIENT VOLTAGE FOR CHARGING**
> A 3S (11.1V nominal) battery pack requires a charging voltage of **12.6V** to reach full capacity.
> * The 6V solar panel's output voltage is too low to feed the TalentCell's charging circuit.
> * Charging this battery from solar would require either a nominal "12V" panel ($V_{mp} \approx 18\text{V}$) or a boost-converter solar controller (MPPT step-up) that raises the panel's voltage to 12.6V.

#### 3. Battery ↔ Metro ESP32-S3
> [!TIP]
> **EXCELLENT DIRECT POWER OPTION**
> You can safely power the Metro ESP32-S3 using the TalentCell's built-in **5V/2A USB port**.
> * Connecting the USB-A port of the TalentCell to the USB-C port of the Metro is plug-and-play. 
> * The TalentCell's internal regulator will efficiently drop the 11.1V battery voltage to a stable 5V for the Metro.
> * **Run Time**: With a capacity of 33.3 Wh, and the Metro drawing between 100mA and 200mA (~0.5W to 1W) while hosting the captive portal, this battery will run the library continuously for **30 to 60 hours** on a single charge.

---

### Conclusion & Operational Recommendation

1.  **Do not use the Solar Panel or the Adafruit bq24074 charger with this battery pack.** 
2.  **To run the library right now**:
    *   Plug the Metro ESP32-S3's USB-C port directly into the TalentCell's 5V USB output.
    *   Use the TalentCell's included 12.6V wall adapter to recharge the battery from mains power when depleted.
3.  **For a true off-grid solar setup**: 
    *   Use a standard **3.7V Lithium-Ion cell** (e.g., Adafruit #5035) with the bq24074 charger and the 6V solar panel.
    *   *Or*, keep the TalentCell battery but replace the 6V panel and bq24074 charger with a **12V panel ($V_{oc} \ge 18\text{V}$)** and a **12V Solar Charge Controller** that has a 12V output.

---

## 2026-07-05: Review of Alternative Battery Chemistries & Form Factors for bq24074

We evaluated alternative battery varieties (including AA rechargeables and bare flat lithium cells) for compatibility with the **Adafruit bq24074 charger** and the **6V solar panel**:

### 1. Flat Lithium Pouch Cells (No Electronics)
*   **Verdict**: **YES (COMPATIBLE)**
*   **Details**: If the flat lithium battery has a nominal rating of **3.7V** (charging to **4.2V**), it is chemically identical to standard Li-Po batteries and 100% compatible with the bq24074.
*   **Safety Precaution**: Since these are "bare leads" with no built-in protection circuit board (PCB), the bq24074 charger will handle the charging logic, but the cell itself has no safety cutoff for overdischarge (draining below 3.0V). Connecting them requires careful handling to avoid short circuits.
*   **Action**: Solder a 2-pin JST-PH connector to the positive (+) and negative (-) leads to plug directly into the charger board.

### 2. Rechargeable AA Batteries (NiMH / NiCd)
*   **Verdict**: **NO (INCOMPATIBLE)**
*   **Details**: Rechargeable AA batteries use Nickel-Metal Hydride (NiMH) or Nickel-Cadmium (NiCd) chemistries, which run at **1.2V nominal**. 
*   **Safety Warning**: The bq24074 is strictly a **Lithium-Ion/Polymer** charger (terminating charge at 4.2V). Attempting to charge NiMH batteries with it will cause them to overheat, leak, vent, or fail catastrophically.

### 3. Cylindrical Lithium-Ion Cells (18650, 21700, 26650)
*   **Verdict**: **YES (COMPATIBLE)**
*   **Details**: These are standard 3.7V nominal Lithium-Ion cells (commonly salvaged from old power banks or laptops). They charge to 4.2V and are fully compatible.
*   **Action**: Use a single cell, or connect multiple cells **strictly in parallel** (all positive leads together, all negative leads together) to multiply capacity while keeping the voltage at 3.7V. *Never connect them in series.*

