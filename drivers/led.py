import json
import machine
from kernel.debug import load_output, debug
import time

# Inicializing and Controling Light output 
def debugging_light(state):
    try:
        def load():
            try:
                with open("/conf/debug_light.conf", "r") as f:
                    data = json.load(f)
            except:
                data = {"Type": "Led", "Pin": "LED"}
                with open("/conf/debug_light.conf", "w") as f:
                    json.dump(data, f)
            return data
        

        data = load()
        if data["Type"] == "Led":
            if data["Pin"] == "LED":
                led = machine.Pin("LED", machine.Pin.OUT)
            else:
                led = machine.Pin(int(data["Pin"]), machine.Pin.OUT)

            if state == "on":
                led.value(1)
                time.sleep(0.2)
                led.value(0)
            elif state == "off":
                led.value(0)
            elif state == "error":
                led.value(1)
                time.sleep(0.2)
                led.value(0)
                time.sleep(0.2)
                led.value(1)
                time.sleep(0.2)
                led.value(0)
        elif data["Type"] == "Neopixel":
            import neopixel

            pin = machine.Pin(int(data["Pin"]), machine.Pin.OUT)

            np = neopixel.NeoPixel(pin, 1)

            if state == "on":
                np.fill((0, 0, 255))
                np.write()
                time.sleep(0.2)
                np.fill((0, 0, 0))
                np.write()
            elif state == "off":
                np.fill((0, 0, 0))
                np.write()
            elif state == "error":
                np.fill((255, 0, 0))
                np.write()
                time.sleep(0.2)
                np.fill((0, 0, 0))
                np.write()
    except Exception as e:
        load_output("false", "Light debbuger", "necesery", "Error: " + str(e))
        debug.error("Light debbuger", str(e))
