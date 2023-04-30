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

# Check if an ADB connection is possible
while ! adb wait-for-device; do
    echo "ADB connection not detected. Please check your phone settings and press enter to try again."
    read -r
done

# Prompt for filtering package list
echo "Enter a keyword to filter the package list, or press enter to list all packages:"
read keyword

# List installed packages and create an indexed array
if [ -z "$keyword" ]; then
    echo "Listing all installed packages..."
    packages_list=($(adb shell pm list packages | sed "s/^package://"))
else
    echo "Listing installed packages containing the keyword '$keyword'..."
    packages_list=($(adb shell pm list packages | grep "$keyword" | sed "s/^package://"))
fi

# Display the packages as a numerical list with versionName
echo "Numerical list of packages:"
for i in "${!packages_list[@]}"; do
    package_name="${packages_list[i]}"
    version_name=$(adb shell dumpsys package "$package_name" | grep 'versionName' | awk '{print $1}' | sed "s/versionName=//")
    echo "$((i + 1)). ${package_name} (versionName: ${version_name})"
done

# Prompt user to select a package by number
echo "Enter the number corresponding to the package you want to extract:"
read package_number

# Validate the input
while [[ $package_number -lt 1 || $package_number -gt ${#packages_list[@]} ]]; do
    echo "Invalid input. Please enter a number between 1 and ${#packages_list[@]}:"
    read package_number
done

# Get the package name from the array
package_name="${packages_list[$((package_number - 1))]}"
version_name=$(adb shell dumpsys package "$package_name" | grep 'versionName' | awk '{print $1}' | sed "s/versionName=//")

# Obtain the APK paths
echo "Getting the APK paths..."
apk_paths=$(adb shell pm path "$package_name" | sed "s/package://" | tr -d '\r')

# Pull the APK files
echo "Extracting the APK files..."
IFS=$'\n' apk_paths_array=($(echo "$apk_paths"))
temp_dir="temp_apk_dir"
mkdir -p "$temp_dir"

for path in "${apk_paths_array[@]}"; do
    file_name="$(basename "$path" | sed "s/^package://")"
    adb pull "$path" "$temp_dir/$file_name"
done

# Merge the APK files into a single APK
echo "Merging the APK files..."
output_file="$(echo "${package_name##*.}" | awk '{print tolower($0)}')-${version_name}.apk"
output_file="${output_file//\//-}"
(
    cd "$temp_dir" || exit
    unzip -qo "$(ls | grep "base.apk")" -d "merged_apk"
    for split_file in $(ls | grep "split_"); do
        unzip -qo "$split_file" -d "temp_split"
        cp -rf "temp_split/"* "merged_apk/"
        rm -rf "temp_split"
    done
    cd "merged_apk" || exit
    zip -qr9 "../$output_file" .
)
mv "$temp_dir/$output_file" .
rm -rf "$temp_dir"

echo "The APK file has been extracted and merged as $output_file."
