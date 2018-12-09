#!/bin/bash
sudo pacman -Sy --noconfirm yaourt htop
yaourt -S --noconfirm sublime-text-dev python-numpy ipython
sudo yaourt -Scc --noconfirm
git init
git config --global user.name "Zotho"
git config --global user.email "svjatoslavalekseef2@gmail.com"