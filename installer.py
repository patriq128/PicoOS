#TODO
# - Finish the apps installing

import subprocess
import os
import shutil
import psutil
import time
import requests
import json
import sys

def pico_exists(path):
    result = subprocess.run(
        ["mpremote", "fs", "ls", path],
        capture_output=True,
        text=True
       )

    return result.returncode == 0

def copy(folder, dont_file=None):
    files = os.listdir(folder)

    for file in files:
        if file == dont_file:
            continue

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

def wait_pico():
    print("Connecting to Pico...")
    while True:
        result = subprocess.run(
            ["mpremote", "connect", "auto", "exec", "print('OK')"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("Device connected")
            break
        else:
            time.sleep(0.5)

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
                print(partition.device, partition.mountpoint)

                names = [
                    "RPI-RP2",
                    "RP2350",
                    "PICO"
                ]

                if any(name in partition.mountpoint.upper() for name in names):
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
    wait_pico()

    result = subprocess.check_output(
       ["mpremote", "exec", "import sys; print(sys.implementation._machine)"]).decode() #type: ignore
    if "Pico W" in result:
        W = True
        print("Pico W")
    else:
        W = False

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
    if W:
        copy("system")
    else:
        copy("system", "app_internet.py")

    print("Installing drivers...")
    if W:
        copy("drivers")
    else:
        copy("drivers", "wifi.py")

    print("Installing main ...")
    subprocess.run(["mpremote", "cp", "main.py", ":"])

def conf():
    result = subprocess.check_output(
        ["mpremote", "exec", "import sys; print(sys.implementation._machine)"]).decode() #type: ignore
    if "Pico W" in result:
        W = True
    else:
        W = False

    print("Configuration time...")
    print("* Press enter for setup default")
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

    if input("Do you have SD card moduule? [Y/n] >> ") == "y":
        print("SD card configuration:")
        print("""How do you want to configure your SD card ?
        1. Manual
        2. Default""")
        sd_configuration = input(">> ")
    

        if  sd_configuration == "1":
            cs = input("cs >> ")
            mosi = input("mosi >> ")
            sck = input("sck >> ")
            miso = input("miso >> ")

            data = {"cs": cs, "mosi": mosi, "sck": sck, "miso": miso}
            os.makedirs("conf", exist_ok=True)
            with open("conf/sd_card.conf", "w") as f:
                json.dump(data, f)
                
        elif sd_configuration == "2":
            data = {"cs": "5", "mosi": "3", "sck": "2", "miso": "4"}
            os.makedirs("conf", exist_ok=True)
            with open("conf/sd_card.conf", "w") as f:
                json.dump(data, f)

    if W:
        print("Do you want to configure WiFi ?")
        ok = input("[Y/n] >> ")
        if ok == "y":
            SSID = input("SSID: ")
            PASSWORD = input("PASSWORD: ")
            autoconnect = input("Enable autoconnect [Y/n]: ")
            if autoconnect == "y":
                autoconnect = True
            else:
                autoconnect = False
        data = []
        data.append({"SSID": SSID, "PASSWORD": PASSWORD, "Autoconnect": autoconnect})
        os.makedirs("conf", exist_ok=True)
        with open("conf/wifi.conf", "w") as f:
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

def apps():
    print("Download apps:")
    manifest = requests.get("https://picoos.dev/download/apps/manifest.json")
    data = manifest.json()
    print("Available apps:")

    apps = []
    selected = []

    a = 0
    for app in data.keys():
        a += 1
        app_name = app.removesuffix(".pcs")
        apps.append(app_name)
        print(f"{a}. [ ] {app_name} - {data[app]['description']}")

    choices = input("Select apps (numbers separated by space): ")

    try:
        choices = [int(x) for x in choices.split()]
    except ValueError:
        print("Invalid input!")
        return

    for choice in choices:
        if 1 <= choice <= len(apps):
            selected.append(apps[choice - 1])
        else:
            print(f"Invalid number: {choice}")

    print("\nSelected apps:")
    for app in apps:
        if app in selected:
            print(f"[X] {app}")
        else:
            print(f"[ ] {app}")
    print("\nDownloading...")

    for app in selected:
        if not os.path.exists(f"install_apps/{app}.pcs"):
            print(f"Downloading {app}.pcs")
            get_file = requests.get(
                f"https://picoos.dev/download/apps/{app}.pcs"
            )
            os.makedirs("install_apps", exist_ok=True)
            with open(f"install_apps/{app}.pcs", "wb") as f:
                f.write(get_file.content)
            print(f"{app} done!")
        else:
            print(f"{app} already exists!")
    print("All apps installed!")
    print("Extracting into device")
    wait_pico()
    subprocess.run(["mpremote", "mkdir", ":install_apps"])
    copy("install_apps")
    for app in selected:
        subprocess.run(["mpremote", "exec", f"from shell.commands import cd; from system.apps import install; cd('install_apps'); install('{app}')"])
    subprocess.run(["mpremote", "exec", "from shell.commands import cd, rm; cd(); rm('install_apps')"])

def main():
    if "--monitor" in sys.argv:
        print("Rebooting system...")
        subprocess.run(["mpremote", "reset"])
        time.sleep(2)
        print("Opening serial monitor...")
        subprocess.run(["mpremote", "repl"])
    elif "--update" in sys.argv:
        print("Updating system...")
        copy_files()
    elif "--apps" in sys.argv:
        apps()
    else:
        print("Welcome to PicoOS installer!")
        print("Follow the intructions")
        print("Good luck!")
        install_micropython()
        copy_files()
        conf()
        apps()
        print("Everything done!")
        print("Rebooting system...")
        subprocess.run(["mpremote", "reset"])
        time.sleep(2)
        print("Opening serial monitor...")
        subprocess.run(["mpremote", "repl"])
if __name__ == "__main__":
    main()
