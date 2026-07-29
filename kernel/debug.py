# FIXME:
# - Repair the sd card shit

from kernel.config import conf, enable

# This is Debugging function and it can save the error messages
class Debugging:

    def save(self, data):
        from drivers.sdcard_driver import sd_card
        sd_status = sd_card.test()
        if sd_status:
            path = "/sd/errors.txt"
        else:
            path = "/errors.txt"

        with open(path, "a") as f:
            f.write(data + "\n")

    def error(self, package, error):
        data = conf.load()
        if not "debugging" in data:
            enable("debugging")

        if data["debugging"] == "enable":
            load = package + ": " + error
            self.save(load)
            print("Saving done")

debug = Debugging()


# This Load staus mainly used on boot
def load_output(state, packate, type_of, text):

    data = conf.load()
    if not "debugging" in data:
        enable("debugging")

    if type_of == "necesery" or data["debugging"] == "enable":
        if state == "ok":
            state_done = " \033[32m OK "
        elif state == "false":
            state_done = "\033[31m FAIL"
        elif state == "info":
            state_done = "\033[90m INFO"
            
        print("\033[0m[  " + state_done + "\033[0m  ]" + "\033[32m" + packate + ":\033[0m " + text)