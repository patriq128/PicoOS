# PicoOS

Terminal-based operating system fully written in MicroPython for the Raspberry Pi Pico family.

[![Website](https://img.shields.io/badge/Website-picoos.dev-pink?style=for-the-badge)](https://picoos.dev)

> **Note:** The installer has only been tested on Linux. Windows and macOS support is expected but has not yet been verified. (Please report any issues if you find them.)

## Features

* **SD card support**
  This is one of the biggest achievements in this operating system. With this, you can expand your storage, download apps and files from your PC to your Pico, or vice versa.

* **Built-in text editor**
  I tried to make it as similar as possible to the original Nano editor. With this, you can easily edit your configuration, write or edit programs locally, and do anything you need with text files.

* **Similarity with Linux**
  I tried to make it feel very similar to Linux, so some of the commands are the same. You can learn Linux while using it.

* **Debugging**
  Debugging this whole system was a pain, so I made several debugging tools:

  * **Light debugging** – Debug what is happening using only a light source such as an LED or NeoPixel.
  * **Boot debugging** – Similar to Linux, you can see what the system is doing while it boots.
  * **Error saving** – Errors can be automatically saved into the internal flash memory or onto the SD card as `errors.txt`.

* **Trun**
  If you want to build a robot or anything that should start immediately without user input, this is for you. Trun is enabled by default, but it does nothing until you create a file called `trun.run` containing the path to the Python program you want to run.

## Repository layout

```text
PicoOS/
├── main.py
├── installer.py
├── requirements.txt
├── kernel/
│   ├── boot.py
│   ├── system.py
│   ├── config.py
│   ├── colors.py
│   └── debug.py
├── shell/
│   ├── terminal.py
│   └── commands.py
├── system/
│   ├── apps.py
│   ├── make_directory.py
│   └── trun.py
├── drivers/
│   ├── led.py
│   ├── sdcard_driver.py
│   └── sdcard.py
└── apps/
    └── nano.py
```

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

### What does the installer do?

I tried to make the installation as simple as possible. The installer does the following for you:

* **Automatically installs MicroPython**
  I know that some people do not know how to install MicroPython on the Pico, so the installer can download the `.uf2` file and install it for you.

* **Copying files**
  The installer automatically creates all required folders and copies all system files.

* **Configuration**
  You do not need to manually edit configuration files. The installer lets you select things like the light source, SD card pins, and whether you want to enable or disable debugging tools.

### Installer commands

I added a few command-line options that you can use:

* **`--update`**
  Skips installing MicroPython and the configuration process, allowing you to update the system files only.

* **`--monitor`**
  If you only want to connect to the serial monitor, this option reboots the Pico and then connects to it.

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
| `touch <file>`      | Create a file                                                                            |
| `ls`                | List files and folders                                                                   |
| `rm <folder/file>`  | Delete a file or folder                                                                  |
| `cat <file>`        | Print the contents of a file                                                             |
| `mv <file>`         | Rename a file                                                                            |
| `mount sd`          | Mount the SD card                                                                        |
| `unmount sd`        | Unmount the SD card                                                                      |
| `install <app>`     | Install an app                                                                           |
| `disable <service>` | Disable a service                                                                        |
| `enable <service>`  | Enable a service                                                                         |
| `sysinfo`           | Print system information                                                                 |
| `<app>`             | Run an installed app                                                                     |

## Configuration

PicoOS has a directory called `conf`, which contains the configuration files.

| File name            | Purpose                                 |
| -------------------- | --------------------------------------- |
| `Configuration.conf` | Service status (enabled/disabled)       |
| `apps.conf`          | App information (name, version, author) |
| `sd_card.conf`       | SD card pin configuration               |
| `debug_light.conf`   | Light type and pin                      |

## How to make your own app

Apps are written in MicroPython.

An app should have at least two definitions:

* **Install**
  This definition allows the installer to get information about the app. The structure should look like this:

  ```python
  def install():
      return {
          "name": "name of the app",
          "version": "version of the app",
          "author": "author of the app"
      }
  ```

* **Main**
  This definition is used to start the program. You can add parameters to the definition, and the system can pass user input to it.

## Built-in text editor

For testing and everyday use, I made a text editor called `nano`. Yes, it's called Nano because I wanted it to be easy to remember.

## Plans for the future

This is the beta version of PicoOS, and it only contains some of the features I want to add.

* **Wi-Fi driver**
  I finally got a Raspberry Pi Pico W, and I want to create an external Wi-Fi driver built on top of the built-in MicroPython driver. I also want to make it reusable for other projects.

* **Wi-Fi communication**
  I want to create something similar to SSH, but simpler and designed specifically for this OS. I plan to write the PC-side application in Rust.

* **Internet browser**
  If I manage to finish the Wi-Fi driver, I want to create a simple web browser so you can browse the internet and do other things.

* **Downloading packages and system updates over the internet**
  One thing I don't like is having to copy files from my PC to the Pico using an SD card. Because of that, I want to create my own server for system updates and applications. This would allow anyone to upload their own apps and download updates directly from PicoOS.

* **Image rendering**
  This may sound like a crazy idea, but I want to create something that can render regular image formats into colored ASCII art so they can be displayed inside the terminal. This could even make it possible to view images from the internet, play videos (which are just lots of images in sequence), or maybe even run simple games like DOOM.
