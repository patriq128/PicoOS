# TODO:
# - Make the comand list as conf file

# FIXME:
# - Delte the wifi things when its not Pico W

import os
from system.apps import apps
from kernel.colors import colors

from shell.commands import echo, hello, clean, exit, cd, python, mkdir, ls, rm, cat, touch, mv, python
from drivers.sdcard_driver import mount, unmount
from kernel.config import enable, disable
from system.apps import install
from kernel.system import system
from drivers.wifi import wifi_driver, ping
from system.app_internet import apps as apps_internet
from system.app_internet import update
def command_list():
    return {
        "echo": echo,
        "hello": hello,
        "clean": clean,
        "exit": exit,
        "cd": cd,
        "python": python,
        "mkdir": mkdir,
        "ls": ls,
        "rm": rm,
        "cat": cat,
        "touch": touch,
        "mv": mv,
        "mount": mount,
        "unmount": unmount,
        "install": install,
        "disable": disable,
        "enable": enable,
        "sysinfo": system,
        "run": python,
        "wifi": wifi_driver,
        "ping": ping,
        "app_install": apps_internet.install,
        "update": update
    }

def terminal():
    commands = command_list()
    while True:
        command = input(os.getcwd() + "\033[32m >> \033[0m")
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
            print("Error:", e)