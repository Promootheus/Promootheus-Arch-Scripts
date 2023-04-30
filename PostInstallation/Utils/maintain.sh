#!/bin/bash

#Refresh Mirrors - note needs to have reflector installed.
#title-Refresh Mirrors
echo -n "Looking For Mirrors...." && sudo reflector -c GB -a 6 --sort rate --save /etc/pacman.d/mirrorlist --verbose


#refresh database

# pacman -Syu
# -S This option is used to synchronize the local package database with the online package database.
# This option should be run before performing any upgrades to ensure that the package database is up to date.

#  -y: This option skips the confirmation prompt and assumes yes for all package installations and upgrades.

# -u: This option is used to upgrade all installed packages to their latest versions.
#title-Pacman Sync+Update
yes | sudo pacman -Syu

#AUR
#title-Yay Sync+Update
yay -Syu

#Clear Package Cache from Arch repositories.
##title-Clear Arch Package Cache
yes | sudo pacman -Sc

#Clear Package Cache from AUR repositories -y autoanswers yes
#title-Clear AUR Package Cache
yes | yay -Sc

#clean up all unwanted dependencies
#title-Remove All Unwanted Dependencies
yes | yay -Yc

#check for orphaned packages

# pacman -Qtdq

#Remove orphaned packages
#title-Remove Orphaned Packages
yes | sudo pacman -Rns $(pacman -Qdtq)

# Clean home cache

# check size of cache with du -sh .cache/
#title-Clear Home Cache
sudo rm -rf .cache/*

#check size of journal log

#du -sh //var/log/journal/

#title-Clear Logs >2Weeks
sudo journalctl --vacuum-time=2weeks

#title-Gimp
yes | sudo pacman -Syu gimp


