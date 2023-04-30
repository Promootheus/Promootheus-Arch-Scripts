#!/bin/bash

# Update System
sudo pacman -Syu
# Update Mirrors+save

# Configure Display
# xrandr --output DP-0 --mode 2560x1440 --rate 120.00

# Install System Tools

yes | sudo pacman -Syu flatpak
yes | sudo pacman -Syu ksysguard
yes | sudo pacman -Syu plasma-wayland-session
yes | sudo pacman -Syu partitionmanager
yay -S --noconfirm stacer
yay -S --noconfirm timeshift

# Utility Tools
yes | sudo pacman -Syu reflector
yes | sudo pacman -Syu ntfs-3g
yes | sudo pacman -Syu spectacle
yes | sudo pacman -Syu filelight
yay -Syu gpu-screen-recorder-git
sudo -H pip install -U oletools[full]

# System Monitoring Tools
yes | sudo pacman -Syu btop

# Network Tools
yes | sudo pacman -Syu wireshark-qt

# NVIDIA Drivers and Tools
yes | sudo pacman -Syu nvidia-inst
nvidia-inst
yay -S --noconfirm nvidia-system-monitor-qt

# Gaming
yes | sudo pacman -Syu steam
yay -S --noconfirm grapejuice
yay -S --noconfirm minecraft-launcher
yay -S --noconfirm heroic-games-launcher-bin
yay -S --noconfirm sidequest

# Audio Tools
yes | sudo pacman -Syu ardour
yes | sudo pacman -Syu audacity

# Video Tools
yes | sudo pacman -Syu obs-studio
yay -S --noconfirm obs-streamfx
yay -S --noconfirm obs-backgroundremoval
yay -S --noconfirm obs-move-transition
yay -S --noconfirm obs-websocket-bin
yay -S --noconfirm keylight-control
yes | sudo pacman -Syu vlc
yes | sudo pacman -Syu kdenlive

# Office Tools
yes | sudo pacman -Syu libreoffice-fresh
yes | sudo pacman -Syu thunderbird
yay -S --noconfirm ttf-ms-fonts
yay -S --noconfirm ttf-google-fonts-git
yay -S --noconfirm 7-zip-full

# Image Tools
yes | sudo pacman -Syu inkscape
yes | sudo pacman -Syu krita
yes | sudo pacman -Syu flameshot
yes | sudo pacman -Syu gimp
yes | sudo pacman -Syu gimp-plugin-gmic

# Download Tools
yes | sudo pacman -Syu qbittorrent
yes | sudo pacman -S uget
yay -S --noconfirm sabnzbd

# Emulators
# yay -S --noconfirm fbzx-git

# Wine and related tools
yes | sudo pacman -Syu wine
yes | sudo pacman -Syu winetricks
yay -S --noconfirm bottles

# Razer Keyboard
yay -S openrazer-meta --noconfirm
sudo gpasswd -a promootheus plugdev
yay -S razergenie --noconfirm
yay -S polychromatic --noconfirm
yay -S razercommander --noconfirm

# Logitech Mouse
sudo pacman -Syu piper

# Development Tools
flatpak install flathub io.github.achetagames.epic_asset_manager
yes | sudo pacman -Syu notepadqq
yay -S --noconfirm visual-studio-code

