import os

from shell.commands import mkdir
from kernel.debug import debug, load_output

# Making apps and cong direcotry if they doesnt exist
def make_basic_directory():
    try:
        if not "apps" in os.listdir():
            mkdir("apps")
            load_output("ok", "Make directory", "necesery", "Making Apps")
        else:
            load_output("false", "Make directory", "not necesery", "Apps already made")
        if not "conf" in os.listdir():
            mkdir("conf")
            load_output("ok", "Make directory", "necesery", "Making Conf")
        else:
            load_output("false", "Make directory", "not necesery", "Conf already made")
    except Exception as e:
        error = "Error: " + str(e)
        load_output("false", "Make directory", "necesery", error)
        debug.error("Make direcotry", str(e))