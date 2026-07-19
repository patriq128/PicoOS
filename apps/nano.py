import os
import sys

def install():
    return {
        "name": "nano",
        "version": "1.1",
        "autor": "ZiDi"
    }

def clean():
    print("\033[2J\033[H", end="")

def main(arg):

    if not arg.startswith("/"):
        arg = os.getcwd().rstrip("/") + "/" + arg

    lines = []

    def load_file():
        try:
            with open(arg, "r") as f:
                for l in f:
                    lines.append(l.rstrip("\n"))
            if not lines:
                lines.append("")
        except OSError:
            lines.append("")

    load_file()

    x = 0
    y = 0

    def render():
        print("\033[2J\033[H", end="")

        for l in lines:
            print(l)

        print("\033[s", end="")
        print(f"\033[{len(lines)+2};1H", end="")
        print("--- Ctrl+Q exit | Ctrl+S save ---", end="")
        print("\033[u", end="")

        print(f"\033[{y+1};{x+1}H", end="")

    def read_char():
        return sys.stdin.read(1)

    render()
    TAB_SIZE = 4
    while True:
        c = read_char()

        if c == "\x11":
            clean()
            break

        elif c == "\x13":
            clean()
            print("\n\n[ SAVED TEXT ]")
            print(arg)
            print("\n".join(map(str, lines)))
            with open(arg, "w") as f:
                f.write("\n".join(map(str, lines)))
            print("\n--- Saved ---")
            break

        if c == "\x1b":
            c2 = read_char()
            c3 = read_char()

            if c2 == "[":
                if c3 == "A":
                    if y > 0:
                        y -= 1
                        x = min(x, len(lines[y]))

                elif c3 == "B":
                    if y < len(lines) - 1:
                        y += 1
                        x = min(x, len(lines[y]))

                elif c3 == "C":
                    x = min(x + 1, len(lines[y]))

                elif c3 == "D":
                    x = max(x - 1, 0)

        elif c in ("\n", "\r"):
            line = lines[y]
            lines[y] = line[:x]
            lines.insert(y + 1, line[x:])
            y += 1
            x = 0

        elif c == "\x7f":
            if x > 0:
                line = lines[y]
                lines[y] = line[:x-1] + line[x:]
                x -= 1

        elif c == "\t":
            line = lines[y]
            spaces = TAB_SIZE - (x % TAB_SIZE)
            lines[y] = line[:x] + (" " * spaces) + line[x:]
            x += spaces

        else:
            line = lines[y]
            lines[y] = line[:x] + c + line[x:]
            x += 1

        render()