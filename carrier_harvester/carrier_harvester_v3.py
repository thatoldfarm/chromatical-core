import os
import struct
import base64
import zlib
from PIL import Image

# --- CONFIGURATION ---
INPUT_PREFIX = "MASTER_DNA_SEED_"
OUTPUT_PNG = "CARRIER_STORAGE_v1.png"
SUBSTRATE_SIZE = 2949120  # 2.88MB ED Floppy Standard
REGISTRY_SIZE = 4096      # 4KB for the file index

def extract_raw_binary_from_png(png_path):
    """Reverses the Pixel-Ligate process to get the raw binary file."""
    img = Image.open(png_path).convert('RGB')
    rgb_data = bytearray(img.tobytes())
    
    end = len(rgb_data) - 1
    while end >= 0 and rgb_data[end] == 0:
        end -= 1
        
    if end < 4: return bytearray() 
    
    b64_len = struct.unpack('>I', rgb_data[end-3:end+1])[0]
    b64_str = rgb_data[:b64_len].decode('ascii').replace('-', '+').replace('_', '/')
    compressed_bin = base64.b64decode(b64_str)
    
    header_len = struct.unpack('>I', compressed_bin[:4])[0]
    payload = compressed_bin[4 + header_len:]
    
    return zlib.decompress(payload, zlib.MAX_WBITS | 16)

def run_packer():
    print(f"--- CHROMIUM CORE: CARRIER HARVESTER V2.1 (SELECTIVE) ---")
    substrate = bytearray([0] * SUBSTRATE_SIZE)
    current_offset = REGISTRY_SIZE
    registry_entries = []

    # Sort files to ensure deterministic offsets
    files = [f for f in sorted(os.listdir('.')) if f.startswith(INPUT_PREFIX) and f.endswith('.png')]
    
    for filename in files:
        print(f"[*] Harvesting: {filename}...")
        try:
            raw_data = extract_raw_binary_from_png(filename)
            short_name = filename.replace(INPUT_PREFIX, "").replace(".png", "")
            
            # --- THE V2.1 FIX: SELECTIVE OPTIMIZATION ---
            original_size = len(raw_data)
            
            # Only optimize Disk Images (which are full of FS padding)
            if any(ext in short_name.lower() for ext in [".img", ".iso"]):
                print(f"    [OPTIMIZE] Stripping nulls from Disk Image...")
                raw_data = raw_data.rstrip(b'\x00')
                # Re-align to 512-byte sectors for floppy compatibility
                padding = (512 - (len(raw_data) % 512)) % 512
                raw_data += b'\x00' * padding
            else:
                # SYSTEM BINARIES (.wasm, .js, .bin) MUST BE BIT-PERFECT
                print(f"    [PASS-THROUGH] Preserving binary integrity...")
            
            size = len(raw_data)
            print(f"    -> Extracted {original_size} bytes. Packed {size} bytes.")

            if current_offset + size > SUBSTRATE_SIZE:
                print(f"    [!] FATAL: {short_name} exceeds Carrier capacity!")
                continue
                
            substrate[current_offset:current_offset + size] = raw_data
            
            # Registry entry: Name (16s), Offset (I), Size (I)
            entry = struct.pack('16sII', short_name[:16].encode('ascii'), current_offset, size)
            registry_entries.append(entry)
            current_offset += size
            
        except Exception as e:
            print(f"    [!] Failed to harvest {filename}: {e}")

    # Write Registry Header (Count + Entries)
    substrate[0:4] = struct.pack('I', len(registry_entries))
    for i, entry in enumerate(registry_entries):
        start = 4 + (i * 24)
        substrate[start:start + 24] = entry

    # Create I/O Membrane (1024 width)
    # R=1(Boot), G=1(Carrier), B=250(WP)
    membrane = bytearray([1, 1, 250] + [0] * (1024 * 3 - 3))
    
    # Forge Carrier PNG (1024x961)
    full_blob = membrane + substrate
    img = Image.frombytes('RGB', (1024, 961), bytes(full_blob))
    img.save(OUTPUT_PNG)
    
    print(f"\n[SUCCESS] Carrier V2.1 Sealed: {OUTPUT_PNG}")
    print(f"[*] Total Files: {len(registry_entries)}")
    print(f"[*] Substrate Usage: {current_offset}/{SUBSTRATE_SIZE} bytes.")

if __name__ == "__main__":
    run_packer()
