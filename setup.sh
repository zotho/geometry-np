#!/bin/bash
sudo pacman -Sy --noconfirm yaourt htop &&
yaourt -S --noconfirm sublime-text-dev python-numpy python-kivy ipython &&
sudo yaourt -Scc --noconfirm &&
git init &&
git config --global user.name "Zotho" &&
git config --global user.email "svjatoslavalekseef2@gmail.com"

# "translate_tabs_to_spaces": true,
# "detect_indentation": false,
# "tab_size": 4