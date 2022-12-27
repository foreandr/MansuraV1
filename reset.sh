mkdir /tmp/mansura
touch /tmp/mansura/ipc.sock

#1. 
source venv/bin/activate
pip install -r requirments.txt

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

