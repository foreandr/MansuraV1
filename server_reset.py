import subprocess

list_files = subprocess.run(["ls", "-a"])
print("The exit code was: %d" % list_files.returncode)

list_files = subprocess.run(["python", "source venv/bin/activate"])
print("The exit code was: %d" % list_files.returncode)

'''
0. source venv/bin/activate
IF CHANGED CLOUD STRUCTURE, RECREATE tmp/mansura/ipc.sock file
IF INSTALLED NEW LIBRARIES
1. pip install -r requirments.txt
IF CHANGE DB
2. python3 database_local.py
3. sudo nginx -s reload 

ps ax|grep gunicorn
4. pkill gunicorn
5. kill -HUP 66173

6. systemctl daemon-reload
7. sudo systemctl start mansura
8. sudo systemctl enable mansura
9. sudo systemctl status mansura
'''