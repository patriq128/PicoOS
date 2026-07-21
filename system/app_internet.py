# FIXME
# - Installing error

import urequests
from system.apps import install
import ujson
import hashlib
import os

class Apps:
    def install(self, app):
        url = f"https://picoos.dev/download/apps/{app}.py"

        try:
            response = urequests.get(url)

            if response.status_code == 200:
                print(f"Installing {app}")
                data = response.text
                with open(f"/{app}.py", "w") as f:
                    f.write(data)

            elif response.status_code == 404:
                print(f"App {app} not existing")

            response.close()

        except Exception as e:
            print(e)

apps = Apps()

def update():
    update = []
    manifest = urequests.get("https://picoos.dev/download/system/manifest.json")
    data = manifest.json()

    def hash_count(path):
        h = hashlib.sha256()

        with open(path, "rb") as f:
            while True:
                chunk = f.read(512)
                if not chunk:
                    break
                h.update(chunk)

        return ''.join('{:02x}'.format(b) for b in h.digest())


    for file in data.keys():

        try:
            current_hash = hash_count("/" + file)

            if current_hash != data[file]:
                update.append(file)

        except OSError:
            print("Missing file:", file)

    if update:
        print("Files to update / install:")
        for code in update:
            print(code)
        respond = input("Continue ? [Y/n]: ")
        if respond == "y":
            for code in update:
                get_file = urequests.get(f"https://picoos.dev/download/system/{code}")
                data = get_file.text
                with open(f"/{code}", "w") as f:
                    f.write(data)
    else:
        print("There is nothing to do")
        print("Everything is upadted :3")