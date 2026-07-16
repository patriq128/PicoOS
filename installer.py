import subprocess
import os
import shutil
import psutil
import time
import requests
import json

def pico_exists(path):
    result = subprocess.run(
        ["mpremote", "fs", "ls", path],
        capture_output=True,
        text=True
       )

    return result.returncode == 0

def copy(folder):
    files = os.listdir(folder)
    for file in files:
        pc_file = os.path.join(folder, file)  # type: ignore
        pico_file = f":{folder}/{file}"
        if pico_exists(pico_file):
            subprocess.run([
                "mpremote",
                "fs",
                "rm",
                pico_file
            ])
        subprocess.run([
            "mpremote",
            "cp",
            pc_file,
            pico_file
        ])

def install_micropython():
    print("""
    1. Raspberry Pi Pico/RP2040 
    2. Raspberry Pi Pico W
    3. Raspberry Pi Pico 2/RP2350
    4. Raspberry Pi Pico 2 W    
    * Skip installing
        """)
    installing = True
    while True:
        rp_type = input(">> ")

        if rp_type == "1":
            board = "RPI_PICO"
            break
        elif rp_type == "2":
            board = "RPI_PICO_W"
            break
        elif rp_type == "3":
            board = "RPI_PICO2"
            break
        elif rp_type == "4":
            board = "RPI_PICO2_W"
            break
        elif rp_type == "*":
            installing = False
            break
        else:
            print("Wrong input!")
            continue

    if installing:
        print("Downloading MicroPython")
        r = requests.get(f"https://micropython.org/download/{board}/{board}-latest.uf2")
        if r.status_code == 200:
            with open("micropython_latest.uf2", "wb") as f:
                f.write(r.content)

            print("Done!")
        else:
            print("Failed:", r.status_code)



        def pico_boot_mode():
            for partition in psutil.disk_partitions():
                if "RPI-RP2" in partition.device or "RPI-RP2" in partition.mountpoint:
                    return True
            return False

        print("Hold boot button and then plug pico into computer")
        while True:
            if pico_boot_mode():
                print("Connected!")
                break

            time.sleep(0.5)
            
        print("Installing micropython into pico")
        for partition in psutil.disk_partitions():
            if "RPI-RP2" in partition.device or "RPI-RP2" in partition.mountpoint:
                print("Found Pico:", partition.mountpoint)

        shutil.copy(
            "micropython_latest.uf2",
            partition.mountpoint
        )

        time.sleep(5)
    else:
        print("Installing skiped")

def copy_files():        
    print("Connecting to Pico...")

    print("Making directorys...")
    subprocess.run(["mpremote", "mkdir", ":apps"])
    subprocess.run(["mpremote", "mkdir", ":drivers"])
    subprocess.run(["mpremote", "mkdir", "kernel"])
    subprocess.run(["mpremote", "mkdir", ":shell"])
    subprocess.run(["mpremote", "mkdir", ":system"])
    subprocess.run(["mpremote", "mkdir", ":conf"])

    print("Installing kernel...")
    copy("kernel")

    print("Installing shell...")
    copy("shell")

    print("Installing system...")
    copy("system")

    print("Installing drivers...")
    copy("drivers")

    print("Installing apps...")
    copy("apps")

    print("Installing main ...")
    subprocess.run(["mpremote", "cp", "main.py", ":"])

    print("Installing nano...")
    data = {"nano": {"Autor": "ZiDi", "Version": "1.1"}}
    os.makedirs("conf", exist_ok=True)
    with open("conf/apps.conf", "w") as f:
        json.dump(data, f)

    print("Configuration time...")
    print("* Press enter for setup default")

def conf():
    print("Led driver:")
    print("""What type of Light do you have ?
    1. Led
    2. Neopixel""")
    led_type = input(">> ")
    if led_type:
        if led_type == "1":
            led_type = "Led"
        elif led_type == "2":
            led_type = "Neopixel"

        print(f"On what Pin its {led_type} connected to?")
        pin = input(">> ")

        data = {"Pin": pin, "Type": led_type}
        os.makedirs("conf", exist_ok=True)
        with open("conf/debug_light.conf", "w") as f:
            json.dump(data, f)

    print("SD card configuration:")
    print("""How do you want to configure your SD card ?
    1. Manual
    2./nothing Default""")
    led_type = input(">> ")

    if led_type and led_type != "2":
        cs = input("cs >> ")
        mosi = input("mosi >> ")
        sck = input("sck >> ")
        miso = input("miso >> ")

        data = {"cs": cs, "mosi": mosi, "sck": sck, "miso": miso}
        os.makedirs("conf", exist_ok=True)
        with open("conf/sd_card.conf", "w") as f:
            json.dump(data, f)

    print("Do you want to disable debbuging mode ?")
    ok = input("[Y/n] >>")
    if ok == "y":
        data = {"debugging": "enable"}
        os.makedirs("conf", exist_ok=True)
        with open("conf/configuration.conf", "w") as f:
            json.dump(data, f)

    if os.path.exists("conf"): #type: ignore
        copy("conf")


def main():
    print("Welcome to PicoOS installer!")
    print("Follow the intructions")
    print("Good luck!")
    install_micropython()
    copy_files()
    conf()
    print("Everything done!")

if __name__ == "__main__":
    main()