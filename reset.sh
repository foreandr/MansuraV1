#!/bin/bash

#mkdir /tmp/mansura
#touch /tmp/mansura/ipc.sock
#sudo chmod 666 /tmp/mansura/ipc.sock

#1. 
. /root/mansura/venv/bin/activate
pip install -r requirements.txt

cd python
python DB_RESET.py
cd ..

# 2.
sudo nginx -s reload 

# 3. 
pkill gunicorn
systemctl daemon-reload
sudo systemctl start mansura
sudo systemctl enable mansura
sudo systemctl status mansura
