import json
import os

# ---- Configuration ----
class Configuration:
    def load(self):
        try:
            try:
                with open("/conf/configuration.conf", "r") as f:
                    return json.load(f)
            except:
                return {}

        except:
            os.makedirs("/conf/configuration.conf")
            return {}

    def save(self, data):
        try:
            os.mkdir("/conf")
        except OSError:
            pass
        with open("/conf/configuration.conf", "w") as f:
            json.dump(data, f)

    def edit(self, name, arg):
        data = self.load()
        data[name] = arg
        self.save(data)

    def new(self, name, arg):
        data = self.load()
        data[name] = arg
        self.save(data)

    def choose(self, name, arg):
        data = self.load()
        if name in data:
            self.edit(name, arg)
        else:
            self.new(name, arg)

conf = Configuration()

def enable(arg):
    conf.choose(arg, "enable")

def disable(arg):
    conf.choose(arg, "disable")