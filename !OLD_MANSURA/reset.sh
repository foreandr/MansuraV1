#!/bin/bash

# SHOULD ALSO AUTOMATE THE GIT CHANGES
#GIT PULL ETC

#0.
mkdir /tmp/mansura
touch /tmp/mansura/ipc.sock

#1. 
source venv/bin/activate
pip install -r requirments.txt


# GIT CHANGES

#. 
python reset.py

# 2.
sudo nginx -s reload 

# 3. 
pkill mansura
systemctl daemon-reload
sudo systemctl start mansura
sudo systemctl enable mansura
sudo systemctl status mansura