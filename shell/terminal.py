import os
import sys
from system.apps import apps
from kernel.colors import colors
from shell.commands import echo, hello, clear, exit, cd, python, mkdir, ls, rm, cat, touch, mv, python, pwd
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
            "clean": clear,
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
        }
    else:
        return {
            "echo": echo,
            "hello": hello,
            "clean": clear,
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
            "app": apps_manager.main
        }

def terminal():
    commands = command_list()
    while True:
        try:
            command = input("\033[0m" + os.getcwd() + "\033[32m >> \033[0m")
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
        except KeyboardInterrupt:
            print("^C")
            continue
        except Exception as e:
            debug.error("Termianl Crash", str(e))
            continue