import machine
import json
import os

from kernel.colors import colors
from kernel.debug import load_output

# ---- SD Card ----
class Sd_card():
    def load(self):
        try:
            with open("/conf/sd_card.conf", "r") as f:
                data = json.load(f)
        except:
            data = {
                "sck": 2,
                "mosi": 3,
                "miso": 4,
                "cs": 5
            }
            with open("/conf/sd_card.conf", "w") as f:
                json.dump(data, f)
        return data

    def configuration(self):
        data = self.load()
        spi = machine.SPI(
            0,
            baudrate=1_000_000,
            polarity=0,
            phase=0,
            sck=machine.Pin(int(data["sck"])),
            mosi=machine.Pin(int(data["mosi"])),
            miso=machine.Pin(int(data["miso"]))
        )

        cs = machine.Pin(int(data["cs"]), machine.Pin.OUT)

        return spi, cs

    def inicializing(self):
        import drivers.sdcard as sdcard

        spi, cs = self.configuration()

        sd = sdcard.SDCard(spi, cs)
        return sd

    def test(self):
        try:
            sd = self.inicializing()
            os.mount(sd, "/sd")
            load_output("ok", "SD_card", "necesery", "SD Card is mounted")
            return True

        except:
            load_output("false", "SD_card", "necesery", "Fail to mount SD Card")
            return False
sd_card = Sd_card()

def mount(arg):
    if arg == "sd":
        sd = sd_card.inicializing()
        os.mount(sd, "/sd")
    else:
        colors.red("Cant mount " + arg)

def unmount(arg):
    try:
        os.umount("/" + arg)
    except:
        colors.red("Cant unmount " + arg)

