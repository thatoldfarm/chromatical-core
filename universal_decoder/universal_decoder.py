import sys
import os
from PIL import Image

def universal_decode(png_path, out_img_path="extracted_data.img"):
    print(f"--- UNIVERSAL PIXEL-LIGATE DECODER V1.0 ---")
    print(f"[*] Analyzing Artifact: {png_path}")
    
    try:
        # 1. Open and Validate Geometry
        img = Image.open(png_path).convert('RGB')
        width, height = img.size
        print(f"[*] Geometry: {width}x{height}")
        
        if width != 800 or height != 616:
            print("[!] WARNING: Non-standard geometry. Results may be unpredictable.")
            
        # 2. Extract Raw Bytes
        raw_bytes = bytearray(img.tobytes())
        
        # 3. Parse I/O Membrane (Row 0: first 2400 bytes)
        membrane = raw_bytes[0:2400]
        r, g, b = membrane[0], membrane[1], membrane[2]
        print(f"[*] I/O Membrane Flags: R={r} (Boot), G={g} (State), B={b} (WP)")
        
        # 4. Extract Substrate (Rows 1-615)
        # 1.44MB Floppy size is exactly 1,474,560 bytes
        floppy_size = 1474560
        substrate = raw_bytes[2400:2400 + floppy_size]
        
        # 5. Text-Check (Heuristic scan for Journey Logs)
        print("[*] Scanning for Text-Soul...")
        try:
            # Check the first 4KB for printable text
            sample = substrate[:4096].rstrip(b'\x00')
            decoded_text = sample.decode('utf-8')
            if len(decoded_text.strip()) > 5:
                print("\n--- [ TEXT DETECTED IN SUBSTRATE ] ---")
                print(decoded_text)
                print("--- [ END OF TEXT SCAN ] ---\n")
        except UnicodeDecodeError:
            print("[*] Substrate appears to be Binary/Compressed data.")

        # 6. Save Binary Image
        with open(out_img_path, 'wb') as f:
            f.write(substrate)
        print(f"[SUCCESS] Raw Substrate saved to: {os.path.abspath(out_img_path)}")

    except Exception as e:
        print(f"[ERROR] Decoding failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python universal_decoder.py <your_pixel_drive.png>")
        sys.exit(1)
    
    universal_decode(sys.argv[1])
