import json
import os
import sys
import hashlib

from shell.commands import touch, rm
from kernel.debug import debug
from system.pcs import pcs


def sha256_file(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        while True:
            data = f.read(512)
            if not data:
                break
            h.update(data)

    return "".join("{:02x}".format(b) for b in h.digest())


class Apps:
    def load(self):
        try:
            with open("/conf/apps.conf", "r") as f:
                return json.load(f)

        except Exception:
            touch("/conf/apps.conf")
            return {}

    def save(self, app):
        data = self.load()
        data.update(app)

        try:
            with open("/conf/apps.tmp", "w") as f:
                json.dump(data, f)

            os.rename("/conf/apps.tmp", "/conf/apps.conf")

        except Exception as e:
            debug.error("Saving apps config failed", str(e))

    def run(self, app, args=None):

        if args is None:
            args = []
        elif not isinstance(args, (list, tuple)):
            args = [args]
        try:
            module_name = "apps." + app + ".main"
            mod = __import__(module_name)
            for part in module_name.split(".")[1:]:
                mod = getattr(mod, part)
        except Exception as e:
            print("Error loading app:", e)
            debug.error("Error loading app", str(e))
            return
        try:
            mod.main(*args)
        except Exception as e:
            print("Error running app:", e)
            debug.error("Error running app", str(e))

apps = Apps()

def install(app):
    if app.endswith(".pcs"):
        app = app[:-4]
    filename = f"{app}.pcs"
    
    try:
        file_hash = sha256_file(filename)
        try:
            with open("/conf/apps.conf", "r") as f:
                data = json.load(f)
        except Exception:
            data = {}
        if app in data:
            if data[app]["Hash"] == file_hash:
                print("Already the newest version")
                return
            else:
                print("Updating")
        else:
            print("Installing")
        pcs(filename)
        with open(f"/apps/{app}/manifest.json", "r") as f:
            info = json.load(f)
        data[app] = {
            "Version": info.get("version", "unknown"),
            "Autor": info.get("autor", "unknown"),
            "Hash": file_hash
        }
        apps.save(data)
    except Exception as e:
        print("Something went wrong:", e)
        debug.error("Error installing app", str(e))

def online_install(app):
    import urequests   # type: ignore
    import ujson       # type: ignore
    if app.endswith(".pcs"):
        app = app[:-4]

    filename = f"{app}.pcs"
    try:
        manifest = urequests.get(
            "https://picoos.dev/download/apps/manifest.json"
        )
        if manifest.status_code != 200:
            print("Manifest download failed")
            manifest.close()
            return
        data = manifest.json()
        manifest.close()

        try:
            with open("/conf/apps.conf") as f:
                conf = ujson.load(f)
        except Exception:
            conf = {}
        remote = data.get(filename)
        if remote is None:
            print("App not exist")
            return
        if app in conf:
            local_hash = conf[app].get("Hash")
            if local_hash == remote.get("hash"):
                print("Already the newest version.")
                return
        print(f"Installing \033[32m{app}\033[0m")
        file = urequests.get(
            f"https://picoos.dev/download/apps/{filename}"
        )
        if file.status_code != 200:
            print("Download failed")
            file.close()
            return
        
        with open(filename, "wb") as f:
            while True:
                chunk = file.raw.read(512)
                if not chunk:
                    break
                f.write(chunk)
        file.close()
        install(app)
        rm(filename)
    except Exception as e:
        print("Online install error:", e)
        debug.error("Online install failed", str(e))

class Apps_manager:
    def install(self, read):
        machine = sys.implementation._machine
        is_wifi = "Pico W" in machine
        if not read.endswith(".pcs"):
            if is_wifi:
                try:
                    import urequests   # type: ignore
                    manifest = urequests.get(
                        "https://picoos.dev/download/apps/manifest.json"
                    )
                    data = manifest.json()
                    manifest.close()

                    if read + ".pcs" in data:
                        online_install(read)
                        return
                except Exception:
                    pass
            try:
                os.stat(f"{read}.pcs")
            except:
                print("The app is not existing")
                return
            install(read)
        else:
            install(read)

    def main(self, arg, arg1=None):
        if arg == "list":
            data = apps.load()
            print("Installed apps:")
            for i in data.keys():
                print(i)
        elif arg == "install":
            if arg1:
                self.install(arg1)
            else:
                print("Missing app name")

apps_manager = Apps_manager()