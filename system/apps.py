import json
import os
from shell.commands import touch, rm, mv
from kernel.colors import colors
from kernel.debug import debug


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

        with open("/conf/apps.conf", "w") as f:
            json.dump(data, f)

    def run(self, app, args=None):
        if args is None:
            args = []
        elif not isinstance(args, (list, tuple)):
            args = [args]

        try:
            module_name = "apps." + app
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
    try:
        module = __import__(app)
        info = module.install()
        data = {
            info["name"]: {
                "Version": info["version"],
                "Autor": info["autor"]
            }
        }

        saved = apps.load()
        exists = app in saved

        if exists:
            old_v = float(saved[app]["Version"])
            new_v = float(data[app]["Version"])

            if old_v < new_v:
                print("Are you sure you want to upgrade \033[32m" + app +
                      " \033[0mfrom version \033[31m" + saved[app]["Version"] +
                      "\033[0mto version \033[34m" + data[app]["Version"] + "\033[0m ?")
            elif old_v == new_v:
                print("App already newest version")
                return
            else:
                print("Are you sure you want to downgrade \033[32m" + app +
                      " \033[0mfrom version \033[31m" + saved[app]["Version"] +
                      "\033[0mto version \033[34m" + data[app]["Version"] + "\033[0m ?")
        else:
            print("Are you sure you want to install \033[32m" + app + " \033[0m?")
        question = input("Type [\033[32my\033[0m/\033[31mn \033[0m] >> ")

        if question == "y":
            apps.save(data)
            app_full = app + ".py"
            if exists:
                rm("/apps/" + app_full)
            mv(app_full, "/apps/" + app_full)

    except Exception as e:
        colors.red("Sorry something went wrong")
        print(e)
        debug.error("Installing", str(e))