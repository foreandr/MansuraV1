from os import access
import subprocess
import json


#TODO: I MAY HAVE TO REMAKE THIS IN LINUX

#sandbox_host_business_email = "sb-o6jo621138414@business.example.com" 
sandbox_host_business_secret = "ENtn7FEGxdghDXvRWOtQGwKforzrGbpZ5t29lpzRObgD4RdQM4o5B-2LIe_nTIVx3Qvq_ZcfEtJvu6yU"
sandbox_host_busniess_client_id = "AZIxbDDf-kzqsvAsiUm1_urviyHJkRAgA4-6R7eAZUwN9PAlQiiOVLubDWInnyomSI9IbT95zlDaWo3N"
#sandbox_app_id = "APP-80W284485P519543T"
#temp_90_min_token = ""

sandbox_user_business_email1 = "111sb-tg3ys21044261@business.example.com"
sandbox_user_business_password1 = 'uE9>W56&' 
sandbox_user_business_account_id= "RRMALYXWT5YMG"

#sandbox_user_personal_email1 = "sb-tg3ys21044261@business.example.com"
#sandbox_user_personal_password1 = 'uE9>W56&' 
#sandbox_user_personal_account_id= "RRMALYXWT5YMG"

#subprocess.run(["python", "curl_test2.py"])

# 1. RUN command to get access token
print("DOING FIRST PART=====================================================\n\n")
subprocess.run([f"test.bat", sandbox_host_busniess_client_id,sandbox_host_business_secret],shell=True)

# 2. GET ACCESS TOKEN
f = open('location.json')
data = json.load(f)
access_token = data["access_token"] 

# 3. USE ACCESS TOKEN FOR TRANSACTION
print("DOING SECOND PART=====================================================\n\n")
subprocess.run([f"test2.bat", access_token, sandbox_user_business_email1],shell=True)