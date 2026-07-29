import os
import sys
import json
import struct
import hashlib


def sha256_file(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            h.update(data)
    return h.hexdigest()


def collect_files(folder):
    files = []

    for root, dirs, filenames in os.walk(folder):
        for file in filenames:
            path = os.path.join(root, file)

            rel = os.path.relpath(path, folder)
            files.append(rel)
    return files


def build_pcs(folder):

    if not os.path.isdir(folder):
        print("Folder not found")
        return


    required = [
        "main.py",
        "manifest.json"
    ]


    for f in required:
        if not os.path.exists(os.path.join(folder, f)):
            print("Missing:", f)
            return

    with open(os.path.join(folder, "manifest.json"),"r") as f:
        manifest = json.load(f)

    app_name = manifest.get("name", os.path.basename(folder))
    output = (app_name + ".pcs").lower()

    print("Building", app_name)

    files = collect_files(folder)

    with open(output, "wb") as out:
        out.write(b"PCS1")
        manifest_data = json.dumps(manifest).encode()
        out.write(struct.pack("<I", len(manifest_data)))
        out.write(manifest_data)
        for file in files:
            path = os.path.join(folder, file)
            data = open(path, "rb").read()

            name = file.encode()
            out.write(struct.pack("<B", len(name)))
            out.write(name)
            out.write(struct.pack("<I", len(data)))
            out.write(data)

            print(" +", file)

    print("\nCreated:", output)
    hash_value = sha256_file(output)
    with open(output + ".sha256", "w") as f:
        f.write(hash_value)

    print("\nSHA256:")
    print(hash_value)



if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: build_app.py <folder>")
    else:
        build_pcs(sys.argv[1])