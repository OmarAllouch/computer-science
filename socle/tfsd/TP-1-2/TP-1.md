# TP 1
> Presented by: Omar Allouch


## Computer Description
Here are the specifications of the computer I'm using:
- Firmware: Asus ZenBook 14X
- OS: Arch Linux x86_64
- Kernel: Linux 6.10.8-arch1-1
- Display: 2880x1800 @ 120 Hz (as 1440x900) in 14.5"
- WM: Hyprland (Wayland)
- Terminal: kitty 0.36.2
- CPU: 13th Gen Intel(R) Core(TM) i7-13700H
- GPU: Iris Xe Graphics
- GPU Driver: i915
- Storage: 512GB SSD
- RAM: 16GB DDR4
- IO Ports: 2x USB-C, 1x USB-A, 1x HDMI port, 1x 3.5mm audio jack


## Program versions
To get the versions of some programs, I wrote a script (`get-versions.sh`) to get all the versions at once.
Here are the versions: (See video for the output)
- Git version:
git version 2.47.0

- Java version:
openjdk version "22.0.2" 2024-07-16
OpenJDK Runtime Environment (build 22.0.2+9)
OpenJDK 64-Bit Server VM (build 22.0.2+9, mixed mode, sharing)

- Maven version:
Apache Maven 3.9.9 (8e8579a9e76f7d015ee5ec7bfcdc97d260186937)
Maven home: /usr/share/java/maven
Java version: 22.0.2, vendor: Arch Linux, runtime: /usr/lib/jvm/java-22-openjdk
Default locale: en_US, platform encoding: UTF-8
OS name: "linux", version: "6.11.2-arch1-1", arch: "amd64", family: "unix"

- Make version:
GNU Make 4.4.1
Built for x86_64-pc-linux-gnu
Copyright (C) 1988-2023 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

- Python version:
Python 3.12.6

- Docker version:
Docker version 27.3.1, build ce1223035a


## Ollama
For the steps 4, 5, and 6, the commands I used are the same as in the shell script (`ask_pdf.sh`), so I'll only show the demonstration of the script in the video.
I ran the script on the file `CV - English.pdf` which is my CV in English, and I asked the question "What does this file contain?".
Here's the output of the script:
```
$ ./ask_pdf.sh CV\ -\ English.pdf "What does this file contain?"
This PDF file appears to contain a resume or CV for Omar All ouch , highlighting his education , professional experience , and skills in the fields of data science and computer science .
```
