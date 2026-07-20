import time

from drivers.sdcard_driver import sd_card
from shell.terminal import terminal
from drivers.led import debugging_light
from system.trun import trun
from shell.commands import clean
from system.make_directory import make_basic_directory
from kernel.system import system
from drivers.wifi import auto_connect
def main():
    time.sleep(3)
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

    # On boot processes 
    system()
    make_basic_directory()
    sd_card.test()
    auto_connect()
    debugging_light("off")
    trun()
    debugging_light("on")
    terminal()
