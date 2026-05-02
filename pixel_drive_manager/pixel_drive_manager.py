# pixel_drive_manager.py
import sys
import math
from PIL import Image

def encode_drive(img_path, png_path, flags=(1, 0, 250)):
    """Converts a 1.44MB .img file into a Pixel Drive .png"""
    print(f"[*] Encoding {img_path} to {png_path}...")
    with open(img_path, 'rb') as f:
        binary_data = bytearray(f.read())
    
    # Pad binary data to fit the 800x615 Substrate exactly
    substrate_bytes_needed = 800 * 615 * 3
    if len(binary_data) < substrate_bytes_needed:
        binary_data += bytearray([0] * (substrate_bytes_needed - len(binary_data)))

    # Create Row 0 (I/O Membrane) - 800 pixels (2400 bytes)
    # Default Flag: Pixel(0,0) = flags. The rest of Row 0 is black (0,0,0)
    membrane_data = bytearray([flags[0], flags[1], flags[2]] + [0] * 2397)

    # Combine Membrane and Substrate
    full_data = membrane_data + binary_data
    
    # Convert to Image
    img = Image.frombytes('RGB', (800, 616), bytes(full_data))
    img.save(png_path)
    print(f"[SUCCESS] Pixel Drive forged: {png_path}")

def decode_drive(png_path, img_path):
    """Extracts a 1.44MB .img file from a Pixel Drive .png"""
    print(f"[*] Decoding {png_path} to {img_path}...")
    img = Image.open(png_path).convert('RGB')
    if img.size != (800, 616):
        raise ValueError("Invalid Geometry. Expected 800x616.")
    
    pixels = bytearray(img.tobytes())
    
    # Read I/O Membrane (Row 0)
    membrane = pixels[:2400]
    print(f"[*] I/O Membrane Flags: R={membrane[0]}, G={membrane[1]}, B={membrane[2]}")
    
    # Extract Substrate (Row 1+) and trim to exact 1.44MB floppy size
    floppy_exact_size = 1474560
    substrate = pixels[2400:2400 + floppy_exact_size]
    
    with open(img_path, 'wb') as f:
        f.write(substrate)
    print(f"[SUCCESS] Floppy extracted: {img_path}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage:")
        print("  python pixel_drive_manager.py encode <in.img> <out.png>")
        print("  python pixel_drive_manager.py decode <in.png> <out.img>")
        sys.exit(1)
        
    mode, in_file, out_file = sys.argv[1], sys.argv[2], sys.argv[3]
    if mode == "encode": encode_drive(in_file, out_file)
    elif mode == "decode": decode_drive(in_file, out_file)
