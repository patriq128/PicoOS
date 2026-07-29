import os
import sys
import json
import struct


def extract_pcs(file):

    if not os.path.exists(file):
        print("File not found")
        return

    with open(file, "rb") as f:

        magic = f.read(4)

        if magic != b"PCS1":
            print("Invalid PCS file")
            return

        manifest_size = struct.unpack("<I", f.read(4))[0]

        manifest = json.loads(f.read(manifest_size).decode())

        app_name = manifest.get("name", "UnknownApp")
        output = app_name

        print("Extracting:", file)
        print("Manifest:")
        print(json.dumps(manifest, indent=4))

        os.makedirs(output, exist_ok=True)

        while True:
            name_length = f.read(1)

            if not name_length:
                break

            name_length = name_length[0]

            filename = f.read(name_length).decode()


            size = struct.unpack("<I", f.read(4))[0]

            data = f.read(size)

            path = os.path.join(output, filename)

            folder = os.path.dirname(path)

            if folder:
                os.makedirs(folder, exist_ok=True)

            with open(path, "wb") as out:
                out.write(data)

            print(" +", filename)
    print("\nDone!")


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: extract_pcs.py <file.pcs>")

    else:
        extract_pcs(sys.argv[1])