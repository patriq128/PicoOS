import time
import sys
from drivers.sdcard_driver import sd_card
from shell.terminal import terminal
from drivers.led import debugging_light
from system.trun import trun
from shell.commands import clean
from system.make_directory import make_basic_directory
from kernel.system import system
from kernel.debug import load_output

def main():
    time.sleep(2)
    print("""
\033[95m⠀⠀⠀⠀⠀⠀⠀⠀⢀⠔⠊⠉⠐⢆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⠏⠀⠀⠀⠀⠘⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣸⠀⠀⠀⠀⠀⠀⢡⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡏⠀⠀⠀⠀⠀⠀⠘⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀\033[95m⢰⠁\033[97m⢀⠔⠀⠒⢤⡔⠈⠉⠢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀\033[95m⣾⠀\033[97m⡇⠀⠀⠂⢀⠂⠀⠂⠀⡅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀\033[95m⡇⠀\033[97m⠑⠤⠀⠠⠊⠐⠤⠤⢞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀\033[95m⢰⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀\033[95m⣼⠀⠀⠀\033[97m⣀⣴⣶⣿⣿⣷⣦⡀\033[95m⢱⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀\033[95m⡇⠀⠀\033[97m⣴⣿⣿⣿⣿⣿⣿⣿⣷\033[95m⡌⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀\033[95m⢰⠁⠀\033[97m⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷\033[95m⡸⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀\033[95m⡾⠀\033[97m⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇\033[95m⢣⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀\033[95m⢠⠇⠀\033[97m⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\033[95m⠈⢆⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀\033[95m⢀⡎⠀⠀\033[97m⠛⠻⠿⠿⠿⠿⠿⣿⣿⠛⠛⠛⠉⠀\033[95m⢰⢆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢠⠏⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠈⠻⣆⠀⠀⠀⠀⠀⠀⠀
⢠⠇⠀⠀⠀⣠⠆⠀⠀⠀⠀⢁⣀⡠⢤⣼⣛⣲⣯⣭⣭⣭⠿⣆⠀⠀⠀⠀⠀⠀
⡎⠀⠀⠀⡰⠃⠀⣀⡤⣖⠪⢿⣶⣿⣿⣿⣿⣿⣿⣿⠿⠟⠀⠘⡄⠀⠀⠀⠀⠀
⣇⠀⠀⡼⣁⢴⡪⠗⠉⠀⠀⠀⠻⠟⢋⣿⣿⣿⣿⣿⡆⠀⠀⠀⢳⠀⠀⠀⠀⠀
⠘⢤⣼⣋⠗⠁⠀⠀⠀⠀⠀⠀⠀⣤⣘⣿⣿⡿⣿⣟⣥⠖⠀⠀⢨⣿⣦⣀⠀⠀
⠀⢸⡗⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⢿⡿⠟⠋⠁⠀⠀⠀⡼⠁⠀⠈⠑⢆
⠀⠀⠳⣀⠀⠀⠀⠀⠀⠀⣠⣦⡀⢠⣄⣠⠤⠷⣀⡠⠶⢄⣀⣼⣀⠀⠀⣀⣀⠜
⠀⠀⠀⠈⠉⠒⠤⠄⣀⣰⣿⣿⣷⣿⡟⠁⠀⠀⠈⠱⡄⠀⠀⠀⠉⠉⠉⠁⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠙⠛⠿⠤⢀⣀⣀⣀⡴⠃⠀\033[0m""")
    print("\nBooting PicoOS")
    result = sys.implementation._machine
    if "Pico W" in result:
        W = True
    else:
        W = False
    # On boot processes 
    system()
    make_basic_directory()
    if sd_card.test() == "mount":
        load_output("ok", "SD_card", "necesery", "SD Card is mounted")
    elif sd_card.test() == "fail":
        load_output("false", "SD_card", "necesery", "Fail to mount SD Card")
    elif sd_card.test() == "notexist":
        load_output("false", "SD_card", "not necesery", "sd_card.conf not exist")
        
    if W:
        from drivers.wifi import auto_connect
        auto_connect()
    debugging_light("off")
    trun()
    debugging_light("on")
    terminal()
