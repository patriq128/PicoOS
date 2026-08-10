import os
import machine #type: ignore
from kernel.colors import colors
from kernel.debug import debug, load_output

# ---- Build In Commands ----
def echo(*args):
    print(" ".join(args))  

def hello():
    print("Hello, world!")
        
def clear():
    print("\033[2J\033[H", end="")
        
def exit():
    print("Good bye!")
    machine.reset()
       
def cd(arg=None):
    if arg == "/" or not arg:
        os.chdir("/")
    elif arg == "..":
        os.chdir("..")
    elif arg in os.listdir():
        os.chdir(arg)
    else:
        colors.red("Path not found")
       
def python(arg):
    if arg in os.listdir():
        try:
            exec(open(arg).read())
        except Exception as e:
            print("Error:", e)
            debug.error("Python", str(e))
    else:
        colors.red("Code " + arg + " not found")

def mkdir(arg):
    os.mkdir(arg)

def pwd():
    print(os.getcwd())
       
def ls(arg=None):
    if arg:
        before = os.getcwd()
        cd(arg)
        for item in os.listdir():
            if not item == "main.py":
                print(item)
        cd(before)
    else:
        for item in os.listdir():
            if not item == "main.py":
                print(item)

def rm(path):
    try:
        stat = os.stat(path)
    except OSError:
        colors.red("File not found")

    if stat[0] & 0x4000:
        for item in os.listdir(path):
            item_path = path + "/" + item
            rm(item_path)

        os.rmdir(path)
        print("folder deleted", path)

    else:
        os.remove(path)
        print("file deleted", path)

def cat(filename):
    with open(filename, "r") as f:
        print(f.read())

def touch(filename):
    open(filename, "w").close()

def cp(src, dst):
    with open(src, "rb") as source:
        with open(dst, "wb") as target:
            while True:
                data = source.read(512)
                if not data:
                    break
                target.write(data)


def mv(src, dst):
    cp(src, dst)
    os.remove(src)