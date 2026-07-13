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
        except:
            touch("/conf/apps.conf")
            return {}

    def save(self, app):
        data = self.load()
        data.update(app)

        with open("/conf/apps.conf", "w") as f:
            json.dump(data, f)

    def run(self, app, arg1):

        try:
            actualpath = os.getcwd()
            module_name = "apps." + app

            mod = __import__(module_name)
                
            for part in module_name.split(".")[1:]:
                mod = getattr(mod, part)

            arg2 = arg1[0] if isinstance(arg1, (list, tuple)) else arg1

            mod.main(actualpath + "/" + arg2)

        except Exception as e:
            print("Error loading app:", e)
            debug.error("Error loading app", str(e))
            print("called error")
            
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
        exists = False
        if app in saved:
            exists = True
            if float(saved[app]["Version"]) < float(data[app]["Version"]):
                print("Are you sure you want to upgrade \033[32m" + app + " \033[0mfrom version \033[31m" + saved[app]["Version"] + "\033[0mto version \033[34m" + data[app]["Version"] + "\033[0m ?")

            if float(saved[app]["Version"]) == float(data[app]["Version"]):
                print("App already newest version")

            if float(saved[app]["Version"]) > float(data[app]["Version"]):
                print("Are you sure you want to downgrade \033[32m" + app + " \033[0mfrom version \033[31m" + saved[app]["Version"] + "\033[0mto version \033[34m" + data[app]["Version"] + "\033[0m ?")
        
            question = input("Type [\033[32my\033[0m/\033[31mn \033[0m] >> ")
        else:
            print("Are you sure you want to install \033[32m" + app + " \033[0m?")

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