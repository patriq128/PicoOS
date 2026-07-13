from kernel.config import conf, enable
from shell.commands import python
from kernel.debug import load_output, debug

import os

# Trun is booting up scripts that are saved in "trun.run"
def trun():
    data = conf.load()
    if not "trun" in data:
        enable("trun")
    if "trun.run" in os.listdir() and data["trun"] == "enable":
        with open("trun.run", "r") as f:
            run = f.read()
            try:
                python(run)
            except Exception as e:
                print("Opening termianl...")
                load_output("false", "Trun", "necesery", "Something went wrong while running it")
                debug.error("Trun", str(e))
    load_output("false", "Trun", "not necesery", "Nothing to load")