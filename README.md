# PicoOS

Terminal-based operating system fully written in MicroPython for Raspberry pi pico family.

[![Website](https://img.shields.io/badge/Website-picoos.dev-pink?style=for-the-badge)](https://picoos.dev)

> Note: The installer has only been tested on Linux. Windows and macOS support is expected but not yet verified. (Please report issuses if you find them)

## Features
- **SD card support** This is one of the biggest success in this operating system. Wtih this you can enlarge you space, download apps and files from your classic PC to your pico or vice versa.
- **Build in text editor** I tryed to make it as similiar as possible as the original nano editor. With this you can simply edit your configuration, lokaly write or edit programs, and everything when you need do something with text files.
- **Similiarity with Linux** Yeah som I tried to make it very simial as Linux so some of the commands are same as on the linux. You can learn why there.
- **Debuging** So debugging this whole system was pain and this is why I made debuging tools as: Light debugging - with this you can debug what is happening only with light source as LED or Nepixel LED; On boot debugging - so this is same as on linux where on booting you can see how its your system doing; Errors saving - so with this the errors can be automaticly saved in to flash memory or into SD card as "errors.txt"
- **Trun** If you want to build robot or anything with code that should boot immediately without user input this is thing for you. Trun its automaticly enabled but it's not working until you make and write into file "trun.run" python code path that you want to run.

## Repository layout

```
PicoOS/
├── main.py                 
├── installer.py             
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

1. Copy this repo:
   ```
   git clone https://github.com/patriq128/PicoOS.git
   ```

2. Enter into folder:
   ```
   cd PicoOS
   ```

3. Install the Python dependencie:
   ```
   pip install -r requirements.txt
   ```

4. Run the installer:
   ```
   python installer.py
   ```
   or
   ```
   python3 installer.py
   ```

5. Follow the promts

### What is this installler doing
I tried to make it simplest as possible so this is things that the installer do for you:

- **Automaticly installing MicroPython** I know some of the peoples doesnt know ho to install micropython to pico so this can download ".uf2" and install it for you
- **Copying** Installer automaticly make folders and copy all of the files
- **Configuration** You dont need to manualy change the conf files with installer you can selct the configuration things as Light source, SD card module pins and if you want not disable debugging tools  

### Some commands for installer
I made some commands that you can use:

- **-- update** This skip installing Micropython and configuration and with this you can update your system codes.
- **-- monitor** If you don't want to connect to serial monitor you can use this script and this reboot and then conenct to pico.