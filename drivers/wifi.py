import network
import time
from kernel.colors import colors
import json
from kernel.debug import load_output
import socket

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

class Saving:
    def load(self):
        try:
            with open("/conf/wifi.conf", "r") as f:
                data = json.load(f)
            return data
        except:
            return False

    def save(self, SSID, PASSWORD, autoconnect):
        try:
            with open("/conf/wifi.conf", "r") as f:
                data = json.load(f)
        except:
            data = []

        data.append({
            "SSID": SSID,
            "PASSWORD": PASSWORD,
            "Autoconnect": autoconnect
        })

        with open("/conf/wifi.conf", "w") as f:
            json.dump(data, f)

        colors.green("Saved")


saving = Saving()

def auto_connect():
    try:
        load_output("info", "WiFi", "necesery", "Connecting to WiFi")
        data = saving.load()

        if not data:
            load_output("false", "WiFi", "necesery", "No WiFi config")
            return

        networks = wlan.scan()

        available = []

        for wifi in data:
            for network in networks:
                ssid = network[0].decode()

                if ssid == wifi["SSID"]:
                    available.append({
                        "SSID": wifi["SSID"],
                        "PASSWORD": wifi["PASSWORD"],
                        "RSSI": network[3]
                    })

        if not available:
            load_output("false", "WiFi", "necesery", "No saved WiFi found")
            return

        available.sort(key=lambda x: x["RSSI"], reverse=True)

        for wifi in available:
            wlan.connect(wifi["SSID"], wifi["PASSWORD"])

            timeout = 10
            while not wlan.isconnected() and timeout > 0:
                time.sleep(1)
                timeout -= 1

            if wlan.isconnected():
                load_output("ok", "WiFi", "necesery", "Connected to " + wifi["SSID"])
                return

        load_output("false", "WiFi", "necesery", "Fail to connect")
    except:
        load_output("false", "WiFi", "necesery", "Something is wrong")

def wifi_driver(command):
    if command == "connect":
        SSID = input("SSID: ")
        PASSWORD = input("Password: ")
        print("Connecting...")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(0.5)
        print("Connected")
        status = input("Do you want to save it [Y/n]: ")
        if status == "y":
            autoconnect = input("DO you want to enable autoconnect [Y/n]: ")
            if autoconnect == "y":
                autoconnect = True
            else:
                autoconnect = False
            saving.save(SSID, PASSWORD, autoconnect)
    elif command == "disconnect":
        wlan.disconnect()
    elif command == "scan":
        for net in wlan.scan():
            print(net[0].decode())
    elif command == "status":
        if wlan.isconnected():
            colors.green("Connected")
            print("IP adress: ", wlan.ifconfig()[0])
        else:
            colors.red("Disconnected")

def ping(host, port=80, count=4, delay=1000):
    try:
        addr_info = socket.getaddrinfo(host, port)[0]
        ip = addr_info[-1][0]
        print("PING", host, "(", ip, ")")
        times = []
        for i in range(count):
            start = time.ticks_ms()

            try:
                s = socket.socket()
                s.settimeout(3)
                s.connect((ip, port))
                s.close()

                end = time.ticks_ms()

                ping_time = time.ticks_diff(end, start)
                times.append(ping_time)

                print("Reply from", ip, "time=", ping_time, "ms"
                )

            except:
                print("Request timeout")

            time.sleep_ms(delay)

        if times:
            avg = sum(times) / len(times)
            print("\n--- Ping statistics ---")
            print("Packets:", len(times))
            print("Average:", avg, "ms")

    except Exception as e:
        print("Ping failed:", e)
