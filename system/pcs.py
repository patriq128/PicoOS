import os
import json
import struct

from shell.commands import mkdir

BLOCK_SIZE = 512


def create_path(path):
    parts = path.split("/")
    current = ""

    for part in parts:
        if not part:
            continue

        current += "/" + part

        try:
            mkdir(current)
        except OSError as e:
            if getattr(e, "errno", None) != 17:
                raise


def copy_file_data(src, dst, size):
    remaining = size
    copied = 0

    with open(dst, "wb") as out:
        while remaining > 0:
            chunk_size = min(BLOCK_SIZE, remaining)
            data = src.read(chunk_size)

            if not data:
                raise Exception("Unexpected end of file")

            out.write(data)

            remaining -= len(data)
            copied += len(data)

            percent = int(copied * 100 / size)
            print(f"\r   {percent}%", end="")

    print()


def pcs(file):
    print(f"\nOpening {file}")

    with open(file, "rb") as package:
        magic = package.read(4)
        if magic != b"PCS1":
            raise Exception("Invalid PCS package")

        manifest_size = struct.unpack("<I", package.read(4))[0]
        manifest_data = package.read(manifest_size)
        manifest = json.loads(manifest_data.decode())

        app_name = manifest.get("name", "UnknownApp")
        app_path = "/apps/" + app_name

        create_path(app_path)

        with open(app_path + "/manifest.json", "w") as manifest_file:
            json.dump(manifest, manifest_file)

        print("Extracting files...")

        while True:
            name_length = package.read(1)

            if not name_length:
                break

            name_length = name_length[0]

            filename = package.read(name_length).decode()
            file_size = struct.unpack("<I", package.read(4))[0]

            output_file = app_path + "/" + filename
            folder = output_file.rsplit("/", 1)[0]

            create_path(folder)

            print(f" - {filename} ({file_size} bytes)")
            copy_file_data(package, output_file, file_size)

        print("\nDone!")