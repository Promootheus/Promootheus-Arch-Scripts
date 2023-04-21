#!/bin/bash

# To get RGB functionality working on the Acer Nitro 5

# Clone the acer-predator-turbo-and-rgb-keyboard-linux-module repository from GitHub
git clone https://github.com/JafarAkhondali/acer-predator-turbo-and-rgb-keyboard-linux-module

# Change the current directory to the cloned repository
cd "acer-predator-turbo-and-rgb-keyboard-linux-module"

# Grant execute permission to all shell scripts in the current directory
chmod +x ./*.sh

# Run the install_service.sh script with superuser privileges to install the systemd service for the keyboard module
sudo ./install_service.sh

# Assign a setting ./facer_rgb.py --help for more
./facer_rgb.py -m 2 -s 3 -b 100

