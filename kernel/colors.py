# Libary for Colored output
class Colors:
    def __getattr__(self, name):
        colors = {
            "red": "\033[31m",
            "green": "\033[32m",
            "blue": "\033[34m",
            "reset": "\033[0m"
        }

        if name in colors:
            def printer(text="TEST"):
                print(colors[name] + text + colors["reset"])
            return printer
        raise AttributeError(name)

colors = Colors()