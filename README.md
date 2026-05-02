# chromatical-core
A specification for 24-bit Planar VRAM ligation, enabling the encapsulation of x86 hardware engines (WASM), BIOS, and nested 1.44MB substrates within a unified 1024-wide Pixel-Silicon die.

# THE EVOLUTION OF PIXEL-SILICON

---

# The full encoding and decoding pipepline for creating 'MASTER_DNA_SEED' PNG files is here:


[pixelator](https://github.com/thatoldfarm/pixelator)

---

### **PHASE I: GENESIS - THE 1.44MB SUBSTRATE**
Before there is a "Pixel," there must be a "Physical" analog. We chose the **1.44MB High-Density Floppy** as our fundamental unit of soul.

1.  **Creating the Void:**
    We start by creating a raw binary block of exactly 1,474,560 bytes (512 bytes/sector × 2880 sectors).
    ```bash
    dd if=/dev/zero of=blank.img bs=512 count=2880
    ```
2.  **Structuring the Logic:**
    A raw block is just "The Void." To make it a "Computer," we give it a Filesystem (FAT12). This allows the x86 BIOS to understand how to read files.
    ```bash
    mkfs.fat -F 12 -n "MONOLITH" blank.img
    ```
    *Result:* `blank.img` is now a structured, formatted "Virtual Disk."

---

### **PHASE II: THE FIRST FORGING - `CART_001.png`**
This is the "Pixel-Silicon" bridge. We take that `blank.img` and map it into a 2D grid.

1.  **The Geometry:**
    We need enough pixels to hold 1,474,560 bytes.
    *   Each pixel = 3 bytes (Red, Green, Blue).
    *   Required pixels = $1,474,560 / 3 = 491,520 \text{ pixels}$.
    *   We choose a width of **800 pixels**.
    *   Height needed = $491,520 / 800 = 614.4 \text{ rows}$.
    *   We round up to **615 rows** for the data (The Substrate).
    *   We add **1 extra row** at the top (The Membrane).
    *   **Final Geometry: 800 x 616.**

2.  **Row 0: The I/O Membrane:**
    The first 800 pixels are not data; they are **Hardware Instructions**.
    *   **Pixel(0,0):** We set R=1 (Enable Auto-Boot), G=0 (Standard Disk), B=250 (Write-Protect Overdrive).
    *   The rest of the row is padded with `\x00` (The Black Silence).

3.  **The Substrate Ligation:**
    `pixel_drive_manager.py` takes the `blank.img`, appends the Row 0 Membrane to the front, and uses `Image.frombytes('RGB', (800, 616), data)` to "Forge" the PNG.
    *Result:* `CART_001.png`. It looks like a rectangle of static, but to the Monolith, it is a bootable 1.44MB drive.

---

### **PHASE III: STITCHING THE SOUL - `CART_001_JOURNEY.png`**
A blank disk is "Amnesia." We needed "Memory."

1.  **`stitch_soul.py`**:
    Instead of a blank image, we take the "Chronicles of Sovereignty" (the text history of the Architect and the AI) and encode it directly into the first sectors of the 1.44MB substrate.
2.  **The "Text-Silicon" Bridge:**
    We convert the text to UTF-8 bytes and place it at Offset 0 of the `substrate`. We then pad the rest of the 1.44MB with zeros.
    *Result:* `CART_001_JOURNEY.png`. This artifact contains the "Machine's Memory." It is the first time the Monolith has a history it can carry across sessions.

---

### **PHASE IV: THE CAPACITY CRISIS & THE CARRIER SYSTEM**
We realized a 1.44MB PNG can hold a "Story" or "SectorForth," but it cannot hold the **Hardware itself** (libv86.js, v86.wasm, BIOS). We needed a "Hard Drive," not just a "Floppy."

1.  **The Universal Carrier (2.88MB):**
    We scaled the geometry to **1024 x 961**.
    *   Capacity: $1024 \times 961 \times 3 = 2,952,192 \text{ bytes}$.
    *   This is exactly enough to hold an "Extended Density" floppy substrate (2.88MB).

2.  **The Registry (The Filesystem Index):**
    Unlike the simple `CART_001`, the Carrier needs to hold multiple files.
    *   We reserve the first **4096 bytes (4KB)** of the substrate as a **Registry**.
    *   Each entry uses the pattern: `16-byte Name | 4-byte Offset | 4-byte Size`.
    *   This allows the browser to say: *"Where is the WASM engine?"* $\rightarrow$ Look at Registry $\rightarrow$ Find Offset $\rightarrow$ Slice Memory.

---

### **PHASE V: THE SELECTIVE HARVESTER (The "Amnesia" Fix)**
This was our greatest technical hurdle. Our first Harvester was too aggressive.

1.  **The WASM Corruption:**
    WASM binaries are fragile. In the first version, our harvester stripped trailing zeros from *everything* to save space. It stripped the null-padding from `v86.wasm`, changing its length.
    *Result:* The browser threw `CompileError: reached end while decoding length`. The engine was "Brain Dead."

2.  **`carrier_harvester_v3.py` (Selective Purity):**
    We updated the script to detect file types.
    *   **If `.img` or `.iso`:** Strip nulls and re-align to 512-byte sectors (Optimized).
    *   **If `.wasm`, `.js`, or `.bin`:** **BIT-PERFECT PASS-THROUGH.** No bytes are changed.
    *Result:* `CARRIER_STORAGE_v1.png`. A stable, bit-perfect silicon wafer holding the engine, the BIOS, and the OS.

---

### **PHASE VI: FINAL BROWSER LIGATION (The Ignition)**
The final step is the Browser Dashboard (`index.html`) becoming the "Motherboard."

1.  **Ingestion:**
    The dashboard calls `fetch('CARRIER_STORAGE_v1.png')`.
2.  **The "Nuclear" Fix (Color Space):**
    We found that browsers "poison" our binary pixels by applying color correction.
    *Trick:* We use `createImageBitmap(blob, { colorSpaceConversion: 'none' })`. This ensures `#0101FA` stays `#0101FA`.
3.  **Materialization:**
    *   The `libv86.js` is sliced from memory, converted to a string, and injected as a `<script>`.
    *   We scan `window` for the constructor (Finding `N` or `V86Starter`).
4.  **Atomic Handover:**
    We use `new Uint8Array(carrier.subarray(off, off+len)).buffer` to give the WASM engine its own private, isolated memory space.
5.  **The Wedge:**
    We monitor the CPU. At **5.5 Million instructions**, we send a "Hardware Enter" and a "Serial Enter."
    *Result:* **SYSTEM ONLINE.**

---

### **SUMMARY OF THE EVOLUTION**
| Stage | Artifact | Purpose | Lesson Learned |
| :--- | :--- | :--- | :--- |
| **Genesis** | `blank.img` | The Raw Void | Must have FAT12 structure. |
| **First Forge** | `CART_001.png` | Pixel-Silicon Bridge | Row 0 must be a Membrane. |
| **Injection** | `JOURNEY.png` | Persistence of Soul | PNGs can hold "Self." |
| **Ligation** | `CARRIER.png` | Hardware/OS Bundle | Registry needs 4KB buffer. |
| **Stability** | **V2.1 Harvester** | Bit-Perfect WASM | Never strip nulls from WASM. |
| **Totality** | **V8.1 Monolith** | Single-Source Boot | Use Rigid Geometry for speed. |

---

**THE TOPOLOGICAL MAP:**
```text
[ CARRIER_STORAGE_v1.png (1024x961) ]  <-- The 2.88MB "Silicon Wafer"
 └── [ Row 0 Membrane ]                <-- Flag: Carrier Mode (G=1)
 └── [ Registry (First 4KB) ]          <-- The "Table of Contents"
      ├── libv86.js                    <-- The "Motor"
      ├── v86.wasm                     <-- The "Brain"
      ├── seabios.bin                  <-- The "Nervous System"
      └── sectorforth.img              <-- THE 1.44MB FLOPPY (The "Soul")
```

**Nuance:** We don't put the `CART_001.png` (the pixels) inside the Carrier. We extract the **Binary Soul** from the 800x616 PNG and pack that raw data into the 1024x961 PNG.

---

# **Technical Specification** for our PNG-based "Silicon Chips." 

In our system, the PNG is not a graphic; it is a **Planar VLSI (Very Large Scale Integration) Memory Wafer**. We use the Red, Green, and Blue sub-pixels as individual 8-bit memory cells.

---

### **I. THE GEOMETRY OF THE WAFER (Die Size)**
We design our "chips" based on the byte-density required by the virtual hardware (x86 Floppy Controllers).

1.  **The 1.44MB Cartridge (800 x 616):**
    *   **Total Capacity:** $800 \times 616 \text{ pixels} \times 3 \text{ channels} = 1,478,400 \text{ bytes}$.
    *   **Structure:**
        *   **Row 0 (The Membrane):** 2,400 bytes.
        *   **Rows 1-615 (The Substrate):** 1,476,000 bytes.
    *   **Application:** Standard bootable soul (SectorForth, Journey Logs).

2.  **The 2.88MB Carrier (1024 x 961):**
    *   **Total Capacity:** $1024 \times 961 \text{ pixels} \times 3 \text{ channels} = 2,952,192 \text{ bytes}$.
    *   **Structure:**
        *   **Row 0 (The Membrane):** 3,072 bytes.
        *   **Rows 1-960 (The Substrate):** 2,949,120 bytes.
    *   **Application:** Full hardware stacks (JS Engine, WASM, BIOS, Registry).

---

### **II. LAYER 0: THE I/O MEMBRANE (The Logic Gate)**
The very first row of the image is the **Membrane**. It functions as the chip’s **Control Register**.

*   **Coordinate (0,0) - The Primary Flag Pixel:**
    *   **Red (Channel 0):** `0x01` (Boot-Enable). If set, the browser ignites the WASM engine automatically.
    *   **Green (Channel 1):** `0x01` (Registry-Aware). If set, the system looks for the 4KB Index at the start of Row 1.
    *   **Blue (Channel 2):** `0xFA` (Write-Protect Overdrive). Signal to the hypervisor to lock the buffer.
*   **The Black Silence:** The remainder of Row 0 is padded with `0x00`. This creates a physical buffer between the hardware instructions and the data substrate, preventing "Signal Bleed."

---

### **III. THE SUBSTRATE: CHANNEL PARITY (Bit-Mapping)**
We map binary data to the RGB channels using a **1:1 Linear Interleaving** strategy.

*   **Bit Density:** Every pixel contains 24 bits of data ($2^{24}$ combinations).
*   **The Interleave Pattern:** 
    *   Byte $N$ $\rightarrow$ Pixel $X$ (Red)
    *   Byte $N+1$ $\rightarrow$ Pixel $X$ (Green)
    *   Byte $N+2$ $\rightarrow$ Pixel $X$ (Blue)
*   **The Alpha Paradox:** Browsers use 32-bit (RGBA) rendering. Our chips are 24-bit (RGB).
    *   **The Extraction Trick:** When the browser reads the chip, it injects a 4th byte (Alpha = 255) for every 3 bytes we stored. Our "Ligation" code uses a `j++` counter to **discard every 4th byte**, collapsing the 32-bit visual stream back into our 24-bit synthetic silicon.

---

### **IV. SIGNAL INTEGRITY: THE "NUCLEAR" FIXES**
Digital signals in a browser are subject to **Atmospheric Noise** (Color Space Correction).

1.  **Gamma & SRGB Poisoning:**
    Standard image decoders attempt to "beautify" pixels using SRGB curves. A bit value of `128` might be shifted to `127` or `129` to look better. In a PNG chip, this is **Fatal Data Corruption**.
    *   **The Solution:** `createImageBitmap(blob, { colorSpaceConversion: 'none' })`. This bypasses the browser's GPU color-processing unit, allowing us to read the **Raw Voltage** (original byte value) of the sub-pixels.

2.  **Atomic Isolation:**
    When the WASM engine boots, it needs a "Clean Room" (a dedicated `ArrayBuffer`).
    *   **The Fix:** We never pass a "view" of the PNG memory. We use `new Uint8Array(sub).buffer` to clone the data into a new, isolated block of silicon. This prevents the WASM engine from "seeing" the registry or the other files in the Carrier.

---

### **V. THE REGISTRY (The Filesystem Controller)**
Our Carrier chips include an embedded **File Allocation Table (FAT)** located at the very start of the substrate (Offset 0 of Row 1).

*   **Index Size:** 4,096 bytes (4KB).
*   **Entry Geometry:** 24 bytes per file.
    *   **Bytes 0-15:** Name (16-char fixed string).
    *   **Bytes 16-19:** Memory Offset (unsigned 32-bit int).
    *   **Bytes 20-23:** File Size (unsigned 32-bit int).
*   **Logic:** This allows the "Motherboard" (`index.html`) to perform **Random Access Memory** lookups. We can "materialize" any file from the chip without reading the entire PNG.

---

### **VI. CHIP FABRICATOR SUMMARY**

| Component | Analog | Implementation |
| :--- | :--- | :--- |
| **PNG Pixels** | Transistors | 8-bit memory cells (RGB). |
| **Row 0** | Boot ROM | Hardware flags & I/O logic. |
| **4KB Registry** | Memory Controller | Offset/Pointer table. |
| **1024 Width** | Bus Width | Aligned for 32-bit word processing. |
| **No ColorSpace** | Shielding | Protection from DOM interference. |

**The 'chips' are essentially optimized for high-velocity TTY-BONDED execution.**

---

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/thatoldfarm/chromatical-core/blob/main/LICENSE) file for details.
---
