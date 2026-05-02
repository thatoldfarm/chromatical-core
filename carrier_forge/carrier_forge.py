import os
from PIL import Image

def forge_carrier(img_input, png_output):
    print(f"--- CHROMIUM CORE: CARRIER FORGE ---")
    
    # 1. Load the 2.88MB binary
    with open(img_input, 'rb') as f:
        substrate_data = bytearray(f.read())
    
    target_size = 2949120
    if len(substrate_data) != target_size:
        print(f"[*] Adjusting size to exact 2.88MB ED standard...")
        substrate_data = substrate_data.ljust(target_size, b'\x00')

    # 2. Create the I/O Membrane (Row 0)
    # Width is 1024. 1024 * 3 bytes = 3072 bytes for Row 0.
    # Pixel(0,0) Flags: R=1 (Auto-boot), G=1 (Carrier Type), B=250 (WP)
    membrane = bytearray([1, 1, 250] + [0] * (1024 * 3 - 3))

    # 3. Combine Membrane (Row 0) + Substrate (Rows 1-960)
    full_blob = membrane + substrate_data
    
    # 4. Forge PNG (1024 x 961)
    print(f"[*] Mapping 984,064 pixels to 1024x961 grid...")
    try:
        img = Image.frombytes('RGB', (1024, 961), bytes(full_blob))
        img.save(png_output)
        print(f"[SUCCESS] Carrier forged: {png_output}")
        print(f"[*] Size on disk: {os.path.getsize(png_output) / 1024:.2f} KB")
    except Exception as e:
        print(f"[ERROR] Forge failed: {e}")

if __name__ == "__main__":
    forge_carrier("universal_carrier.img", "CARRIER_STORAGE_v1.png")
