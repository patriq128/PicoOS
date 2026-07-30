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
        print("Folder not found:", folder)
        return

    required = [
        "main.py",
        "manifest.json"
    ]

    for file in required:
        if not os.path.exists(os.path.join(folder, file)):
            print("Missing:", file)
            return

    manifest_path = os.path.join(folder, "manifest.json")

    try:
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
    except json.JSONDecodeError:
        print("Invalid manifest.json")
        return

    app_name = manifest.get(
        "name",
        os.path.basename(os.path.abspath(folder))
    )

    output = (app_name + ".pcs").lower()
    output_dir = os.path.join("builds", app_name)
    output_path = os.path.join(output_dir, output)

    os.makedirs(output_dir, exist_ok=True)

    print("Building", app_name)

    files = collect_files(folder)

    with open(output_path, "wb") as out:
        out.write(b"PCS1")

        manifest_data = json.dumps(
            manifest,
            separators=(",", ":")
        ).encode()

        out.write(struct.pack("<I", len(manifest_data)))
        out.write(manifest_data)

        for file in files:
            path = os.path.join(folder, file)

            with open(path, "rb") as f:
                data = f.read()

            name = file.encode()

            out.write(struct.pack("<B", len(name)))
            out.write(name)
            out.write(struct.pack("<I", len(data)))
            out.write(data)

            print(" +", file)

    hash_value = sha256_file(output_path)
    hash_path = output_path + ".sha256"

    with open(hash_path, "w") as f:
        f.write(hash_value)

    print("\nCreated:", output_path)
    print("\nSHA256:")
    print(hash_value)
    print("\nHash saved:", hash_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: build_app.py <folder>")
        sys.exit(1)

    build_pcs(sys.argv[1])