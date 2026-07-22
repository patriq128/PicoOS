# FIXME
# - Installing error

import urequests
from system.apps import install
import ujson
import hashlib
import os
import sys
from system.apps import apps as apps_saving

def hash_count(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        while True:
            chunk = f.read(512)
            if not chunk:
                break
            h.update(chunk)

    return ''.join('{:02x}'.format(b) for b in h.digest())


def apps(command, app):
    if command == "update":
        manifest = urequests.get("https://picoos.dev/download/apps/manifest.json")
        data = manifest.json()
        try:
            os.stat(f"/apps/{app}.py")
            exist = True
        except:
            exist = False
        if exist:
            if hash_count(f"/apps/{app}.py") != data[app]:
                print(f"Updating \033[32m{app}\033[0m")
                get_file = urequests.get(f"https://picoos.dev/download/apps/{app}.py")
                data = get_file.text
                with open(f"/apps/{app}.py", "w") as f:
                    f.write(data)
                get_file.close()
            else:
                print("App already updated")
        else:
            print(f"App {app} not installed.")
        manifest.close()

    elif command == "install":
        manifest = urequests.get("https://picoos.dev/download/apps/manifest.json")
        data = manifest.json()
        if app in data:
            try:
                os.stat(f"/apps/{app}.py")
                exist = True
            except:
                exist = False
            if exist:
                if hash_count(f"/apps/{app}.py") == data[app]:
                    print(f"App \033[32m{app}\033[0m already installed and updated")
                else:
                    print(f"Updating \033[32m{app}\033[0m")
                    get_file = urequests.get(f"https://picoos.dev/download/apps/{app}.py")
                    data = get_file.text
                    with open(f"/apps/{app}.py", "w") as f:
                        f.write(data)
                    get_file.close()
            else:
                print(f"Installing \033[32m{app}\033[0m")
                get_file = urequests.get(f"https://picoos.dev/download/apps/{app}.py")
                data = get_file.text
                with open(f"/apps/{app}.py", "w") as f:
                    f.write(data)
                get_file.close()
                sys.path.append("/apps")

                module = __import__(app)
                info = module.install()

                data = {
                    info["name"]: {
                        "Version": info["version"],
                        "Autor": info["autor"]
                    }
                }
                apps_saving.save(data)
        manifest.close()

def update():
    update = []
    manifest = urequests.get("https://picoos.dev/download/system/manifest.json")
    data = manifest.json()

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
            print("\033[32m", code)
        respond = input("\033[0mContinue ? [Y/n]: \033[0m")
        if respond == "y":
            for code in update:
                print(f"Downloading\033[32m {code}\033[0m")
                get_file = urequests.get(f"https://picoos.dev/download/system/{code}")
                data = get_file.text
                with open(f"/{code}", "w") as f:
                    f.write(data)
            print("\033[32m Done :)\033[0m")
            get_file.close()
    else:
        print("There is nothing to do")
        print("Everything is upadted :3")
    manifest.close()
