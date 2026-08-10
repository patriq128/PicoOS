# PicoOS

Terminal-based operating system fully written in MicroPython for the Raspberry Pi Pico family.

[![Website](https://img.shields.io/badge/Website-picoos.dev-pink?style=for-the-badge)](https://picoos.dev)

> **Note:** The installer has only been tested on Linux. Windows and macOS support is expected but has not yet been verified. (Please report any issues if you find them.)

## Features

* **SD card support**
  With this, you can expand your storage, download apps and files from your PC to your Pico, or vice versa. I am very happy that I made this.

* **WiFi connectivity**
  When you have a Raspberry Pi Pico W, the installer and system automatically detect it and install the WiFi drivers and enable WiFi connectivity.

* **Apps**
  PicoOS has its own app system called `pcs`. You can install apps with 3 methods: Internet, Locally, or With Installer.
  > For now I have built 2 apps: "nano" - Text editor, "image" - Image render

* **Similarity with Linux**
  I tried to make it feel very similar to Linux, so some of the commands are the same.

* **Debugging**
  Debugging this whole system was a pain, so I made several debugging tools:

  * **Light debugging** – Debug what is happening using only a light source such as an LED or NeoPixel.
  * **Boot debugging** – Similar to Linux, you can see what the system is doing while it boots.
  * **Error saving** – Errors can be automatically saved into the internal flash memory or onto the SD card as `errors.txt`.

* **Trun**
  If you want to build a robot or anything that should start immediately without user input, this is for you. Trun is enabled by default, but it does nothing until you create a file called `trun.run` containing the path to the Python program you want to run.

* **Installer**
   I wanted to make this OS much easier to install, so I made an external installer.

## Repository layout

```text
PicoOS/
├── main.py #because MicroPython automatically runs main.py, I made this file and it just runs the boot process
├── installer.py #with this script PicoOS is installed and configured
├── requirements.txt #Python dependencies for the installer
├── manifest.json #version of each file in this system
├── kernel/
│   ├── boot.py #running boot sequences and printing the ASCII logo
│   ├── system.py #prints all information about the system
│   ├── config.py #system services configuration
│   ├── colors.py #library for colored text
│   └── debug.py #debugging messages during boot and saving errors
├── shell/ 
│   ├── terminal.py #the whole shell system
│   └── commands.py #built-in commands
├── system/
│   ├── apps.py #app runner and installer
│   ├── make_directory.py #creates basic directories if they don't exist
│   ├── pcs.py #extractor for pcs apps
│   ├── system_update.py #system updater using internet - install only on W version
│   └── trun.py #automatically runs Python code after boot
├── external_tools/
│   ├── build_app.py #this tool builds a pcs app and sha256 key from the app folder
│   ├── extract_app.py #this tool extracts pcs into a folder
│   └── pxi_converter.py #this converts an image into a ".pxi" image file
├── drivers/
│   ├── led.py #light debugging
│   ├── sdcard_driver.py #SD card driver built on the SD card library
│   ├── sdcard.py #library for SD cards
│   └── wifi.py #the WiFi tools use the network library - install only on W version
└── apps/
    ├── image.pcs #app for image rendering
    └── nano.pcs #text editor similar to the original Linux nano editor
```
> **The SD card driver used in PicoOS is based on the MicroPython SD card library:** https://github.com/micropython/micropython-lib/blob/master/micropython/drivers/storage/sdcard/sdcard.py
## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/patriq128/PicoOS.git
   ```

2. Enter the project folder:

   ```bash
   cd PicoOS
   ```

3. Install the Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the installer:

   ```bash
   python installer.py
   ```

   or

   ```bash
   python3 installer.py
   ```

5. Follow the prompts.

> **Note:** On Linux, I recommend using `sudo`.

### What does the installer do?

I tried to make the installation as simple as possible. The installer does the following for you:

* **Automatically installs MicroPython**
  I know that some people do not know how to install MicroPython on the Pico, so the installer can download the `.uf2` file and install it for you.

* **Copying files**
  The installer automatically creates all required folders and copies all system files.

* **Configuration**
  You do not need to manually edit configuration files. The installer lets you select things like the light source, SD card pins, and whether you want to enable or disable debugging tools.

* **Installing apps**
  You can install apps externally using the installer.

* **Serial monitor**
  This reboots the system and connects to the device using serial.

### Installer commands

I added a few command-line options that you can use:

* **`--update`**
  Skips installing MicroPython and the configuration process, allowing you to update the system files only.

* **`--monitor`**
  If you only want to connect to the serial monitor, this option reboots the Pico and then connects to it.

* **`--apps`**
  Install apps externally.

## Built-in commands

Most of the commands are very similar to Linux.

| Command             | What it does                                                                             |
| ------------------- | ---------------------------------------------------------------------------------------- |
| `echo <text>`       | Print text                                                                               |
| `clean`             | Clear the display                                                                        |
| `exit`              | Exit the OS (soft reboot)                                                                |
| `cd <folder>`       | Change directory. `cd /` goes to the home directory and `cd ..` goes one directory back. |
| `python <file>`     | Run a Python file                                                                        |
| `mkdir <folder>`    | Create a folder                                                                          |
| `pwd`               | Show what path you are in                                                                |
| `touch <file>`      | Create a file                                                                            |
| `ls`                | List files and folders                                                                   |
| `rm <folder/file>`  | Delete a file or folder                                                                  |
| `cat <file>`        | Print the contents of a file                                                             |
| `mv <file>`         | Rename a file                                                                            |
| `mount sd`          | Mount the SD card                                                                        |
| `unmount sd`        | Unmount the SD card                                                                      |
| `app <command>`     | Commands are `install`, `list`                                                           |
| `disable <service>` | Disable a service                                                                        |
| `enable <service>`  | Enable a service                                                                         |
| `sysinfo`           | Print system information                                                                 |
| `<app>`             | Run an installed app                                                                     |
| `wifi <command>`    | Commands are: `connect`, `status`, `disconnect` -- available only on the W version       |
| `ping`              | Ping the website or IP address -- available only on the W version                        |
| `update`             | Update the system -- available only on the W version                                    |

## Hardware Configuration

One of the features of PicoOS is support for external hardware connectivity.

You can configure your hardware during installation or later through configuration files.

### Default Hardware Configuration

The following configuration is used by default for supported hardware.

#### SD Card

| SD Card Pin | GPIO Pin |
| ----------- | -------- |
| CS          | 5        |
| MOSI        | 3        |
| SCK         | 2        |
| MISO        | 4        |

## Configuration

PicoOS has a directory called `conf`, which contains the configuration files.

| File name            | Purpose                                 |
| -------------------- | --------------------------------------- |
| `Configuration.conf` | Service status (enabled/disabled)       |
| `apps.conf`          | App information (name, version, author) |
| `sd_card.conf`       | SD card pin configuration               |
| `debug_light.conf`   | Light type and pin                      |
| `wifi.conf`          | WiFi information                        |

## How to make your own app

Apps are written in MicroPython.

The app's main file should be named `"main.py"` and have a `main` definition, which is what the app runner executes. You also need a `manifest.json`, formatted like this:
```
{
  "name": "name of the app",
  "version": "version of the app",
  "author": "author of the app"
}
``` 
Then you can use the external tool `"build_app.py"` to convert your app folder into a pcs app.
Usage: ```python build_app.py <folder_path>```. After this, you'll find your pcs file and its hash in `external_apps/build/app_name/`.

## Plans for the future

This is the beta version of PicoOS, and it only contains some of the features I want to add.

* **Wi-Fi communication**
  I want to create something similar to SSH, but simpler and designed specifically for this OS. I plan to write the PC-side application in Rust.

* **Internet browser**
  If I manage to finish the Wi-Fi driver, I want to create a simple web browser so you can browse the internet and do other things.

* **Public app system**
  For now, the apps you download externally are made by me, but I want to open this whole system up to other authors.

* **Ethernet module**
  PicoOS supports external Ethernet modules, allowing you to connect to the Internet without requiring a Pico W.

## Why I made this
I got the idea for this project one day when I wanted to try installing Linux on the RP2040, but that's not possible because of the small amount of RAM and flash memory. So I said to myself, "Why not make my own OS for the Raspberry Pi Pico?" And that's how the project started.