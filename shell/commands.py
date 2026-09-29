import os
import machine #type: ignore
from kernel.colors import colors
from kernel.debug import debug, load_output
import hashlib
import json

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
    if not arg:
        os.chdir(f"/home/{userman.get()}")
    if arg == "/":
        os.chdir("/")
    elif arg == "..":
        os.chdir("..")
    elif arg in os.listdir():
        os.chdir(arg)
       
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

def rm(path, argument=None):
    do = True
    if path == "/" and argument != "--no-preserve-root":
        print("""rm: refusing to remove '/'.
rm: use --no-preserve-root to override this protection.""")
        do = False
    if argument == "--no-preserve-root":
        colors.red(f"WARNING: This will permanently delete '{path}'.")
        if input("Continue ? [y/N] >>") == "y":
            do = True
        else:
            do = False

    if do:
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

# User manager
class UserMan:

    def __init__(self):
        try:
            os.mkdir("/home")
        except OSError:
            pass

    def __call__(self, do, *items):
        if do == "new":
            self.new(*items)
        elif do == "login":
            self.login()

    def load(self):
        try:
            with open("/conf/users", "r") as f:
                loaded = json.load(f)
        except Exception as e:
            print(e)
            open("/conf/users", "w").close()
            loaded = {}

        return loaded

    def save(self, name, password):
        loaded = self.load()

        password_hash = hashlib.sha256(password.encode()).digest().hex()
        home = f"/home/{name}"

        loaded[name] = {
            "password": password_hash,
            "home": home
        }

        with open("/conf/users", "w") as f:
            json.dump(loaded, f)

    def new(self, name, password=None):
        try:
            os.mkdir(f"/home/{name}")
        except:
            print(f"Folder '{name}' already exists")

        if password is None:
            password = input("New password >> ")

        try:
            self.save(name, password)
            print(f"Created user: {name}")
        except Exception as e:
            colors.red("something went wrong")
            print(e)

    def check_password(self, name, password):
        users = self.load()

        if name not in users:
            return False

        password_hash = hashlib.sha256(password.encode()).digest().hex()

        return password_hash == users[name]["password"]

    def login(self):
        global user
        name = input("Username: ")
        password = input("Password: ")
        if self.check_password(name, password):
            print("Login successful!")
            user = name
            try:
                os.chdir(f"/home/{user}")
            except:
                os.mkdir(f"/home/{name}")
                os.chdir(f"/home/{user}")

            return True

        else:
            print("Wrong password!")
            return False

    def get(self):
        return user

userman = UserMan()