#!/bin/bash

# Check if ADB is installed
if ! command -v adb &> /dev/null; then
    # Install ADB
    echo "Installing ADB..."
    sudo pacman -Syu android-tools
else
    echo "ADB is already installed."
fi

# Enable USB debugging on your Android device manually
echo "On your Android device, enable USB debugging by going to Settings > About phone > Software information and tapping on the Build number seven times. Then, go back to Settings > Developer options and toggle on USB debugging."

echo "Please connect your Android device to your computer using a USB cable."

# List installed packages
echo "Listing installed packages..."
adb shell pm list packages

# Get package name from the user
echo "Enter the package name of the app you want to extract (e.g., com.microsoft.emmx for Microsoft Edge):"
read package_name

# Obtain the APK path
echo "Getting the APK path..."
apk_path=$(adb shell pm path "$package_name" | sed "s/^package://")

# Pull the APK file
echo "Enter the desired output file name (e.g., output_file.apk):"
read output_file
echo "Extracting the APK file..."
adb pull "$apk_path" "$output_file"

echo "The APK file has been extracted as $output_file."
