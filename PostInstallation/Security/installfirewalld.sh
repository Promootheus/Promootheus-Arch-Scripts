#!/bin/bash

#First, open a terminal and ensure your Arch Linux system is up-to-date:

sudo pacman -Syu

# Next, install Firewalld using the following command:

sudo pacman -S firewalld

# Enable and start Firewalld:

# After installing Firewalld, enable it to start automatically on system boot:

sudo systemctl enable firewalld

#Then, start the Firewalld service:

sudo systemctl start firewalld

#Install the KDE Plasma System Tray Applet for Firewalld:

sudo pacman -S plasma-firewall
