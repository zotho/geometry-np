#!/bin/bash
cd ../../
git add *
git commit -a -m $1
# git remote set-url origin git@github.com:zotho/geometry-np.git
# eval "$(ssh-agent -s)"
# ssh-keygen -t rsa
# ssh-add ~/.ssh/id_rsa
git push origin master