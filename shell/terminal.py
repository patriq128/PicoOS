import os
import sys
from system.apps import apps
from kernel.colors import colors
from shell.commands import echo, hello, clean, exit, cd, python, mkdir, ls, rm, cat, touch, mv, python, pwd, userman
from drivers.sdcard_driver import mount, unmount
from kernel.config import enable, disable
from system.apps import apps_manager
from kernel.system import system
from kernel.debug import debug
result = sys.implementation._machine
if "Pico W" in result:
    W = True
else:
    W = False
if W:
    from drivers.wifi import wifi_driver, ping
    from system.system_update import update
def command_list():
    if W:
        return {
            "echo": echo,
            "hello": hello,
            "clear": clean,
            "exit": exit,
            "cd": cd,
            "python": python,
            "mkdir": mkdir,
            "pwd": pwd,
            "ls": ls,
            "rm": rm,
            "cat": cat,
            "touch": touch,
            "mv": mv,
            "mount": mount,
            "unmount": unmount,
            "disable": disable,
            "enable": enable,
            "sysinfo": system,
            "run": python,
            "wifi": wifi_driver,
            "ping": ping,
            "app": apps_manager.main,
            "update": update,
            "userman": userman
        }
    else:
        return {
            "echo": echo,
            "hello": hello,
            "clear": clean,
            "exit": exit,
            "cd": cd,
            "python": python,
            "mkdir": mkdir,
            "pwd": pwd,
            "ls": ls,
            "rm": rm,
            "cat": cat,
            "touch": touch,
            "mv": mv,
            "mount": mount,
            "unmount": unmount,
            "disable": disable,
            "enable": enable,
            "sysinfo": system,
            "run": python,
            "app": apps_manager.main,
            "userman": userman
        }

def terminal():
    commands = command_list()
    while True:
        path = os.getcwd()
        home = f"/home/{userman.get()}"

        if path == home:
            path = "~"
        elif path.startswith(home + "/"):
            path = "~" + path[len(home):]
            
        text = "\033[32m" + userman.get() + "@PicoOS" + "\033[0m:" + "\033[34m" + path + "\033[0m$ "
        command = input(text)
        part = command.split()
        if not part:
            continue
        name = part[0]
        argument = part[1:]
        try:
            if name in commands:
                commands[name](*argument)
            else:
                try:
                    apps.run(name, argument)
                except Exception:
                    colors.red("Command " + name + " not found.")

        except Exception as e:
            debug.error("Command Crash", str(e))
            continue
