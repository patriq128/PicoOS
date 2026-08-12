import machine #type: ignore
import json
import os

from kernel.colors import colors

# ---- SD Card ----
class Sd_card():
    def load(self):
        try:
            with open("/conf/sd_card.conf", "r") as f:
                data = json.load(f)
        except:
            data = None
        return data

    def configuration(self):
        data = self.load()
        if data:
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
        else:
            return None, None

    def inicializing(self):
        import drivers.sdcard as sdcard
        if self.load():
            spi, cs = self.configuration()

            sd = sdcard.SDCard(spi, cs)
            return sd

    def test(self):
        if self.load():
            try:
                sd = self.inicializing()
                os.mount(sd, "/sd")
                return "mount"

            except:
                return "fail"
        else:           
            return "notexist"
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

