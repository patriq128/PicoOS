from PIL import Image
import struct
import sys
import os

if len(sys.argv) > 1:
    file = sys.argv[1]
else:
    file = input("File path >> ")

if len(sys.argv) > 2:
    width = int(sys.argv[2])
else:
    width = 80

name = os.path.splitext(os.path.basename(file))[0].lower()

img = Image.open(file).convert("RGB")

height = int(img.height * width / img.width)

img = img.resize((width, height))

with open(f"{name}.pxi", "wb") as f:

    f.write(b"PXI1")

    f.write(struct.pack(">HH", width, height))

    for y in range(height):
        for x in range(width):
            r,g,b = img.getpixel((x,y))
            f.write(bytes([r,g,b]))