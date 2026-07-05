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

---

## 2026-07-05: Review of 3.7V 110mAh Small Battery Compatibility

We evaluated the suitability of using a small **3.7V 110mAh Li-Po battery** for this project.

### 1. Voltage Compatibility
*   **Verdict**: **COMPATIBLE**
*   **Details**: The nominal voltage (3.7V) and chemistry are a perfect match for the bq24074 charger.

### 2. Runtime Math (Metro ESP32-S3)
*   **Capacity**: 110mAh (0.11 Ah / ~0.4 Wh)
*   **Current Draw**: The Metro ESP32-S3 draws between **100mA and 150mA** when running the captive portal server and broadcasting Wi-Fi.
*   **Calculation**:
    $$\text{Runtime} = \frac{110\text{ mAh}}{120\text{ mA}} \approx 0.9\text{ hours} \approx 55\text{ minutes}$$
*   **Conclusion**: A fully charged 110mAh battery will only power the Metro for **about 45 to 60 minutes** before draining.

### 3. Safety Warning: Charge Rate ($C$-rate)
*   **Verdict**: > [!CAUTION]
    > **UNSAFE TO CHARGE WITHOUT MODIFICATION**
    > * Lithium batteries of this size should be charged at **1C or less** for safety (1C for a 110mAh battery is **110mA**).
    > * The Adafruit bq24074 board is pre-configured with a charge current resistor setting of **500mA**. 
    > * Charging a 110mAh battery at 500mA is a **4.5C charge rate**. This is extremely dangerous and can cause the small battery to overheat, swell (puff up), leak, or catch fire.
*   **Recommendation**: Do not connect this tiny battery to the bq24074 charger unless you desolder and replace the charging program resistor on the board to limit the output current to $\le 100\text{mA}$.

---

## 2026-07-05: Sizing a Battery for 24-Hour Continuous Operation

We calculated the minimum battery capacity and safety margins required to maintain continuous Wi-Fi broadcasting and web serving for a full 24-hour period.

### 1. The Power Budget Math
*   **Average Metro ESP32-S3 Current Draw ($I_{\text{draw}}$)**: 
    *   *Baseline*: ~120mA (when broadcasting AP with minor traffic).
    *   *Active Peak*: ~150mA (spikes up to 240mA during page requests/transmits).
*   **Target Runtime ($t$)**: 24 hours
*   **Minimum Theoretical Capacity**:
    *   At 120mA draw: $120\text{mA} \times 24\text{h} = 2,880\text{mAh}$
    *   At 150mA draw: $150\text{mA} \times 24\text{h} = 3,600\text{mAh}$

### 2. Sizing with a Safety Margin (25%)
To ensure reliable operation under colder temperatures, battery degradation over time, and the standard cut-off limits of battery protection circuits (which cut off around 3.0V, leaving ~5-10% of nominal charge unused), we apply a **25% safety buffer**:
*   **Conservative Target Capacity (120mA baseline)**: $\approx \mathbf{3,600\text{mAh}}$
*   **High-Traffic Target Capacity (150mA active)**: $\approx \mathbf{4,500\text{mAh}}$

---

### 3. Recommended Battery Options (All 3.7V / 4.2V max)

Since the Adafruit bq24074 board charges at **500mA** by default, these larger capacities will charge at a highly safe and gentle rate ($<0.15\text{C}$).

#### Option A: Cylindrical 18650 Cells (Easy to Salvage or Buy)
*   **Single High-Capacity Cell**: A single high-grade 18650 cell (e.g. Sanyo/Panasonic NCR18650B) provides **3400mAh–3500mAh**. This meets the 24-hour minimum baseline but has a thin safety margin.
*   **2x 18650 Cells in Parallel**: Connecting two standard 18650 cells (e.g. 2600mAh each) in parallel yields **5200mAh**.
    *   *Runtime*: **35 to 43 hours** of continuous broadcasting.
    *   *Verdict*: This is the **ideal hobbyist sweet spot** for cost, size, and safety margin.

#### Option B: Pre-Assembled Flat Li-Po Packs (Plug-and-Play)
*   **3.7V 4400mAh Li-Po** (e.g., Adafruit #358): Double-cell pouch pack with JST-PH connector.
    *   *Runtime*: **29 to 36 hours** of continuous operation.
*   **3.7V 6600mAh Li-Po** (e.g., Adafruit #353): Triple-cell pouch pack.
    *   *Runtime*: **44 to 55 hours** of continuous operation.
*   **3.7V 10050mAh Li-Ion** (e.g., Adafruit #5035): Triple-cell cylindrical block (original BOM item).
    *   *Runtime*: **70 to 80+ hours** (almost 3 full days of completely dark autonomy).



