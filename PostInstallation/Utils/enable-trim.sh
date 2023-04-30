#!/bin/bash

# Check for hdparm
if ! command -v hdparm &> /dev/null
then
    echo "hdparm is not installed. Installing now..."
    sudo pacman -S hdparm
fi

# Check for TRIM capability
echo "Checking for TRIM capability using hdparm..."
if sudo hdparm -I /dev/sda | grep -i TRIM &> /dev/null
then
    # Check if TRIM is enabled
    if sudo systemctl status fstrim.timer | grep -i active &> /dev/null
    then
        echo "TRIM is already enabled. You don't need to do anything."
    else
        echo "Enabling TRIM..."
        sudo systemctl enable fstrim.timer
        sudo systemctl start fstrim.timer
        echo "TRIM enabled. All done."
    fi
else
    echo "Your device does not support TRIM."
fi
