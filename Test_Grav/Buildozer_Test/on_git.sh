#!/bin/bash
cd ../../
git add *
git commit -a -m $1
git remote set-url origin git@github.com:zotho/geometry-np.git
git push origin master