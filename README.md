# PicoOS

A lightweight, terminal-based operating environment for the Raspberry Pi Pico family, written in MicroPython. PicoOS boots into a colored shell with a small set of built-in commands, a simple app system, SD card support, and a PC-side installer that flashes MicroPython and deploys the whole project to the board in one step.

[![Website](https://img.shields.io/badge/Website-picoos.dev-pink?style=for-the-badge)](https://picoos.dev)
> Note: The installer has only been tested on Linux. Windows and macOS support is expected but not yet verified.
## Features

- **Interactive shell** – a command-line REPL with built-in file, directory, and system commands
- **App system** – drop a `.py` file with an `install()` and `main()` function into the project and load it as a shell command
- **SD card support** – mount/unmount an SD card over SPI, with configurable pins
- **Status light** – a configurable LED or NeoPixel used as a boot/error indicator
- **Persistent configuration** – JSON config files under `/conf` for the light, SD card, installed apps, and general flags
- **Autorun** – optionally execute a script (`trun.run`) automatically before dropping into the shell
- **Error logging** – failures are optionally logged to the SD card (or flash if no SD card is present)
- **One-command installer** – a PC-side script that flashes MicroPython, copies every file over `mpremote`, and walks you through configuration

## Supported hardware

- Raspberry Pi Pico / Pico W (RP2040)
- Raspberry Pi Pico 2 / Pico 2 W (RP2350)
- An SPI SD card module (optional)
- An onboard/external LED or a NeoPixel (optional, used for status indication)

## Repository layout

```
PicoOS/
├── main.py                  # Entry point run automatically by MicroPython
├── installer.py             # PC-side installer (flashes MicroPython + deploys files)
├── kernel/
│   ├── boot.py               # Boot sequence
│   ├── system.py             # Prints system/CPU/RAM/flash info
│   ├── config.py             # JSON-backed configuration store
│   ├── colors.py             # ANSI color helpers
│   └── debug.py              # Error logging and status output
├── shell/
│   ├── terminal.py           # Shell loop and command dispatch
│   └── commands.py           # Built-in commands
├── system/
│   ├── apps.py                # App loading/installing
│   ├── make_directory.py      # Creates /apps and /conf on first boot
│   └── trun.py                 # Runs an autostart script if enabled
├── drivers/
│   ├── led.py                 # Status light driver (LED or NeoPixel)
│   ├── sdcard_driver.py        # SD card mounting via SPI
│   └── sdcard.py               # SPI SD card block driver
└── apps/
    └── nano.py                 # A small text editor app
```

## Installation

The installer runs on your computer and talks to the Pico over USB via [`mpremote`](https://docs.micropython.org/en/latest/reference/mpremote.html).

1. Install the Python dependencies:
   ```
   pip install mpremote psutil requests
   ```
2. Connect the Pico to your computer.
3. Run the installer from the project root:
   ```
   python installer.py
   ```
4. Follow the prompts:
   - Choose your board (`RPI_PICO`, `RPI_PICO_W`, `RPI_PICO2`, `RPI_PICO2_W`) to download and flash the latest MicroPython firmware, or skip this step if MicroPython is already installed.
   - The installer creates the required directories on the board and copies `kernel/`, `shell/`, `system/`, `drivers/`, `apps/`, and `main.py`.
   - Finish the configuration wizard to set the status light type/pin, SD card pins, and whether debug logging is enabled. Pressing Enter at each step keeps the defaults.

On boot, MicroPython automatically runs `main.py`, which hands off to `kernel/boot.py`.

## Installer details

`installer.py` has three modes, selected by command-line flag:

| Command | Behavior |
|---|---|
| `python installer.py` | Full setup: flash MicroPython, copy all project files, run the configuration wizard, then reset the board and open a serial monitor |
| `python installer.py --update` | Re-copy `kernel/`, `shell/`, `system/`, `drivers/`, `apps/`, and `main.py` without reflashing MicroPython or reconfiguring |
| `python installer.py --monitor` | Reset the board and open a serial monitor (`mpremote repl`) without copying anything |

### What each step does

- **`install_micropython()`** – prompts for a board type, downloads the matching `.uf2` from `micropython.org`, waits for the Pico to appear in BOOTSEL mode (detected via `psutil.disk_partitions()`), and copies the `.uf2` to it. Entering `*` skips this step if MicroPython is already installed.
- **`copy_files()`** – creates `/apps`, `/drivers`, `kernel`, `/shell`, `/system`, and `/conf` on the board over `mpremote`, then copies each project folder and `main.py`. It also writes a default `conf/apps.conf` entry registering the bundled `nano` app.
- **`conf()`** – the configuration wizard. Prompts for the status light type/pin (writes `conf/debug_light.conf`), SD card pins (writes `conf/sd_card.conf`), and whether to enable debug logging (writes `conf/configuration.conf`). Pressing Enter at any prompt skips that file, leaving PicoOS to fall back on its built-in defaults. Any files written are copied to the board's `/conf` at the end.

## Boot sequence

1. Clear the screen and print the startup logo.
2. Print system information (`kernel/system.py`): OS release, machine, CPU frequency, RAM, and flash usage.
3. Create `/apps` and `/conf` if they don't exist yet.
4. Attempt to mount an SD card, if configured.
5. Run `trun.run` at the filesystem root if autorun is enabled and the file exists.
6. Blink the status light.
7. Start the interactive shell.

## Shell commands

| Command | Description |
|---|---|
| `echo <text>` | Print text |
| `hello` | Print a greeting |
| `clean` | Clear the screen |
| `exit` | Reset the board |
| `cd <path>` | Change directory |
| `python <file>` | Execute a MicroPython script |
| `mkdir <name>` | Create a directory |
| `ls` | List the current directory |
| `rm <path>` | Remove a file or directory |
| `cat <file>` | Print a file's contents |
| `touch <file>` | Create an empty file |
| `mv <src> <dst>` | Rename/move a file |
| `mount sd` | Mount the SD card |
| `unmount <name>` | Unmount a mounted volume |
| `install <app>` | Install an app from the current directory into `/apps` |
| `enable <flag>` / `disable <flag>` | Toggle a configuration flag |

Any command that isn't built in is looked up as an installed app under `/apps`.

## Configuration

Settings are stored as JSON under `/conf`:

| File | Purpose |
|---|---|
| `configuration.conf` | General flags, e.g. `debugging` and `trun` (autorun) |
| `debug_light.conf` | Status light `Type` (`Led` or `Neopixel`) and `Pin` |
| `sd_card.conf` | SPI pins for the SD card: `sck`, `mosi`, `miso`, `cs` |
| `apps.conf` | Registry of installed apps and their versions |

If a config file is missing, sensible defaults are generated automatically (status light on pin 25, SD card on pins `sck=2, mosi=3, miso=4, cs=5`).

### Autorun

Place a script at `trun.run` in the root of the filesystem. If the `trun` flag is enabled, it runs once at boot, before the shell starts.

## Writing an app

An app is a single `.py` file placed in `apps/` (or copied to the board and installed with `install <name>`). It must define:

```python
def install():
    return {
        "name": "myapp",
        "version": "1.0",
        "autor": "your_name",
    }

def main(path):
    # path is the absolute path passed as the command's argument
    ...
```

Once installed, the app can be run from the shell by typing its name followed by an argument, for example:

```
nano notes.txt
```

`apps/nano.py` is a working example: a minimal line-based text editor supporting arrow-key navigation, tab insertion, and save/quit via `Ctrl+S` / `Ctrl+Q`.

## Error logging

When `debugging` is enabled, failures raised by the kernel, drivers, or apps are appended to `errors.txt` — on the SD card if one is mounted, otherwise on the board's internal flash.
