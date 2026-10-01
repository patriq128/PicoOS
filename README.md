# PicoOS

Terminal-based operating system fully written in MicroPython for the Raspberry Pi Pico family.

[![Website](https://img.shields.io/badge/Website-picoos.dev-pink?style=for-the-badge)](https://picoos.dev)

> **Note:** The installer has only been tested on Linux. Windows and macOS support is expected but has not yet been verified. Please report any issues you encounter.

<img src="assets/screenshot.png">

## Features

* **SD card support**
  This allows you to expand your storage, download apps and files from your PC to your Pico, or vice versa. I am very happy that I made this.

* **Wi-Fi connectivity**
  When you have a Raspberry Pi Pico W, the installer and system automatically detect it, install the Wi-Fi drivers, and enable Wi-Fi connectivity.

* **Apps**
  PicoOS has its own app system called `pcs`. You can install apps using three methods: Internet, Local, or Installer.

  > For now, I have built two apps: `nano` – a text editor, and `image` – an image renderer.

* **Similarity to Linux**
  I tried to make it feel very similar to Linux, so some of the commands are the same.

* **Debugging**

  Debugging this whole system was a pain, so I made several debugging tools:

  * **Light debugging** – Debug what is happening using only a light source such as an LED or NeoPixel.

  * **Boot debugging** – Similar to Linux, you can see what the system is doing while it boots.

  * **Error saving** – Errors can be automatically saved to the internal flash memory or to the SD card as `errors.txt`.

* **Trun**
  If you want to build a robot or anything that should start immediately without user input, this is for you. Trun is enabled by default, but it does nothing until you create a file called `trun.run` containing the path to the Python program you want to run.

* **Users**
  The old version didn't have this, but because I want this OS to feel very much like Linux, I decided to add it.

* **Installer**
  I wanted to make this OS much easier to install, so I made an external installer.

## Repository layout

```text
PicoOS/
├── main.py # Because MicroPython automatically runs main.py, I made this file to start the boot process.
├── installer.py # This script installs and configures PicoOS.
├── requirements.txt # Python dependencies for the installer.
├── manifest.json # Version of each file in the system.
├── kernel/
│   ├── boot.py # Runs the boot sequence and prints the ASCII logo.
│   ├── system.py # Prints all information about the system.
│   ├── config.py # System services configuration.
│   ├── colors.py # Library for colored text.
│   └── debug.py # Debugging messages during boot and error saving.
├── shell/
│   ├── terminal.py # The entire shell system.
│   └── commands.py # Built-in commands.
├── system/
│   ├── apps.py # App runner and installer.
│   ├── make_directory.py # Creates basic directories if they don't exist.
│   ├── pcs.py # Extractor for PCS apps.
│   ├── system_update.py # System updater using the Internet – install only on the W version.
│   └── trun.py # Automatically runs Python code after boot.
├── external_tools/
│   ├── build_app.py # This tool builds a PCS app and generates its SHA-256 hash from the app folder.
│   ├── extract_app.py # This tool extracts PCS files into a folder.
│   └── pxi_converter.py # This tool converts an image into a `.pxi` image file.
├── drivers/
│   ├── led.py # Light debugging.
│   ├── sdcard_driver.py # SD card driver built on the SD card library.
│   ├── sdcard.py # Library for SD cards.
│   └── wifi.py # Wi-Fi tools using the network library – install only on the W version.
└── apps/
    ├── image.pcs # App for image rendering.
    └── nano.pcs # Text editor similar to the original Linux nano editor.

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
  You do not need to manually edit configuration files. The installer lets you select things like the light source, SD card pins, users, and whether you want to enable or disable debugging tools.

* **Installing apps**
  You can install apps externally using the installer.

* **Serial monitor**
  This reboots the system and connects to the device using serial.

### Installer commands

I added a few command-line options that you can use:

* **`--update`**
  Skips installing MicroPython and the configuration process, allowing you to update only the system files.

* **`--monitor`**
  If you only want to connect to the serial monitor, this option reboots the Pico and then connects to it.

* **`--apps`**
  Installs apps externally.

## Built-in commands

Most of the commands are very similar to Linux.

| Command             | What it does                                                                              |
| ------------------- | ----------------------------------------------------------------------------------------- |
| `echo <text>`       | Print text                                                                                |
| `clear`             | Clear the display                                                                         |
| `exit`              | Exit the OS (soft reboot)                                                                 |
| `cd <folder>`       | Change directory. `cd /` goes to the home directory, and `cd ..` goes one directory back. |
| `python <file>`     | Run a Python file                                                                         |
| `mkdir <folder>`    | Create a folder                                                                           |
| `pwd`               | Show the current path                                                                     |
| `touch <file>`      | Create a file                                                                             |
| `ls`                | List files and folders                                                                    |
| `rm <folder/file>`  | Delete a file or folder                                                                   |
| `cat <file>`        | Print the contents of a file                                                              |
| `mv <file>`         | Rename a file                                                                             |
| `mount sd`          | Mount the SD card                                                                         |
| `unmount sd`        | Unmount the SD card                                                                       |
| `app <command>`     | Commands are `install` and `list`                                                         |
| `disable <service>` | Disable a service                                                                         |
| `enable <service>`  | Enable a service                                                                          |
| `sysinfo`           | Print system information                                                                  |
| `<app>`             | Run an installed app                                                                      |
| `wifi <command>`    | Commands are `connect`, `status`, and `disconnect` – available only on the W version      |
| `ping`              | Ping a website or IP address – available only on the W version                            |
| `update`            | Update the system – available only on the W version                                       |
| `userman <command>` | Work with users. Commands are `new` and `login`                                           |

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
| `wifi.conf`          | Wi-Fi information                       |

## How to make your own app

Apps are written in MicroPython.

The app's main file sh
