from os import access
import subprocess
import json

sandbox_host_business_secret = "EK0-nbaBiL-NBxk3-jhckyKWdAVd0WD4n-bf825UCJW0rILCk4WlBP8o8Zt0OqbbmifpYewXIuuHs0Jt"
sandbox_host_busniess_client_id = "AYQLIdaKdimWeGBm2GA-sQKJEMeFxMHtutYMwIGEA92gQSAGJb-9d1oyksP9MozKYSspppmB70KIxb4v"

outgoing_email = "foreandr@gmail.com"

# 1. RUN command to get access token
print("DOING FIRST PART=====================================================\n\n")
subprocess.run([f"test.bat", sandbox_host_busniess_client_id,sandbox_host_business_secret],shell=True)

# 2. GET ACCESS TOKEN
f = open('location.json')
data = json.load(f)
access_token = data["access_token"] 
print("ACCESS TOKEN:",access_token)

# 3. USE ACCESS TOKEN FOR TRANSACTION
print("DOING SECOND PART=====================================================\n\n")
subprocess.run([f"test2.bat", access_token, outgoing_email],shell=True)