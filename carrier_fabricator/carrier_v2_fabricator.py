import os
import struct
import base64
import zlib
from PIL import Image

# --- CONFIGURATION V2 ---
OUTPUT_PNG = "CARRIER_STORAGE_v2.png"
SUBSTRATE_SIZE = 12582912  # 12MB SUBSTRATE (Wafer Scale)
REGISTRY_SIZE = 8192       # 8KB for a larger Registry

def extract_raw_binary_from_png(png_path):
    """Reverses the Pixel-Ligate process to get the raw binary file."""
    if not png_path.startswith("MASTER_DNA_SEED_"):
        # If it's our already forged Carrier V1, read it as raw RGB bytes
        img = Image.open(png_path).convert('RGB')
        # Skip Row 0 Membrane
        pixels = list(img.getdata())
        width, height = img.size
        # Extract RGB (3 bytes per pixel) starting from Row 1
        return bytearray([b for p in pixels[width:] for b in p])

    # Otherwise, it's a DNA SEED (B64/Gzip)
    img = Image.open(png_path).convert('RGB')
    rgb_data = bytearray(img.tobytes())
    end = len(rgb_data) - 1
    while end >= 0 and rgb_data[end] == 0: end -= 1
    b64_len = struct.unpack('>I', rgb_data[end-3:end+1])[0]
    b64_str = rgb_data[:b64_len].decode('ascii').replace('-', '+').replace('_', '/')
    compressed_bin = base64.b64decode(b64_str)
    header_len = struct.unpack('>I', compressed_bin[:4])[0]
    return zlib.decompress(compressed_bin[4 + header_len:], zlib.MAX_WBITS | 16)

def run_v2_packer():
    print(f"--- CHROMICAL CORE: CARRIER FABRICATOR V2 (NESTED) ---")
    substrate = bytearray([0] * SUBSTRATE_SIZE)
    current_offset = REGISTRY_SIZE
    registry_entries = []

    # THE BATCH: Carrier V1 + The Linux Seeds
    targets = [
        "CARRIER_STORAGE_v1.png",
        "MASTER_DNA_SEED_bzImage.png",
        "MASTER_DNA_SEED_rootfs.cpio.gz.png"
    ]
    
    for filename in targets:
        if not os.path.exists(filename):
            print(f"[!] Error: {filename} missing. Skipping.")
            continue
            
        print(f"[*] Nesting: {filename}...")
        try:
            raw_data = extract_raw_binary_from_png(filename)
            size = len(raw_data)
            
            # Use short name for registry
            short_name = filename.replace("MASTER_DNA_SEED_", "").replace(".png", "")
            
            if current_offset + size > SUBSTRATE_SIZE:
                print(f"[!] FATAL: {short_name} exceeds V2 capacity!")
                continue
                
            substrate[current_offset:current_offset + size] = raw_data
            
            # Registry: Name(16s), Offset(I), Size(I)
            entry = struct.pack('16sII', short_name[:16].encode('ascii'), current_offset, size)
            registry_entries.append(entry)
            print(f"    -> Ligation: {size} bytes at {current_offset}")
            current_offset += size
        except Exception as e:
            print(f"    [!] Failed {filename}: {e}")

    # Write V2 Registry
    substrate[0:4] = struct.pack('I', len(registry_entries))
    for i, entry in enumerate(registry_entries):
        start = 4 + (i * 24)
        substrate[start:start + 24] = entry

    # Create V2 Membrane (1024 width) - G=2 signifies V2 Hyper-Carrier
    membrane = bytearray([1, 2, 250] + [0] * (1024 * 3 - 3))
    
    # Forge V2 (1024 width, 4097 height to fit 12.5MB)
    full_blob = membrane + substrate
    img = Image.frombytes('RGB', (1024, 4097), bytes(full_blob))
    img.save(OUTPUT_PNG)
    print(f"\n[SUCCESS] Hyper-Carrier V2 Sealed: {OUTPUT_PNG}")
    print(f"[*] Final Efficiency: {current_offset}/{SUBSTRATE_SIZE} bytes used.")

if __name__ == "__main__":
    run_v2_packer()
