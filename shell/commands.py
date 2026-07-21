import os
import machine
from kernel.colors import colors
from kernel.debug import debug, load_output

# ---- Build In Commands ----
def echo(*args):
    print(" ".join(args))  

def hello():
    print("Hello, world!")
        
def clean():
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
       
def ls():
    for item in os.listdir():
        if not item == "main.py":
            print(item)

def rm(path):
    if path in os.listdir(): 
        if os.stat(path)[0] & 0x4000:  
            for f in os.listdir(path):
                os.remove(path + "/" + f)
            os.rmdir(path)
            print("folder deleted:", path)
        else:
            os.remove(path)
            print("file deleted:", path)
    else:
        colors.red("File not found")

def cat(filename):
    with open(filename, "r") as f:
        print(f.read())

def touch(filename):
    open(filename, "w").close()

def mv(first, second):
    os.rename(first, second)