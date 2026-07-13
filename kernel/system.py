import gc
import os
import machine

def system():
    info = os.uname()
    print("System:", info.sysname)
    print("Release:", info.release)
    print("Machine:", info.machine)
    print("CPU freq: ", machine.freq())

    gc.collect()
    total = gc.mem_free() + gc.mem_alloc()
    print("Total RAM:", total, "bytes")

    stat = os.statvfs("/")
    flash_size = stat[0] * stat[2]
    flash_free = stat[0] * stat[3]
    print("Flash size:", flash_size)
    print("Flash free:", flash_free)