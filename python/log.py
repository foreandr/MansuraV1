try:    
    import python.MODULES as modules
except:
    import MODULES as modules
    
from datetime import datetime
import pytz

def log_function(msg_type, log_string, vote_type="None", distro_type="None", session_user="", function_name=""):
    #if log_string == "write() argument must be str, not None":
    #    print("got here")
    #    return "" # THIS ERROR CAN BE IGNORED
    # print(f"TESTING:{log_string}")
    
    my_accounts = ['', 'mazinosarchive','youtubebot', 'Admin']

    my_time = pytz.timezone('US/Eastern') 
    current_datetime = datetime.now(my_time).replace(microsecond=0).replace(tzinfo=None)
    current_date = current_datetime.strftime('%Y-%m-%d')
    err_string = f"[{current_datetime}][{msg_type}][{function_name}][{session_user}]-{log_string}\n" 

    if msg_type == "error":
        # CHECK IF RESET QUERY
        if "CREATE_TABLE" not in err_string or "relation" not in err_string:        
            print("==========LOGGING AN ERROR PLS NOTICE!=========")
        log_path = f"/root/mansura/logs/errors/{current_date}.txt"
        with open(f'{log_path}', 'a') as f:
            f.write(err_string)

    elif msg_type == "request":
        if session_user in my_accounts:
            with open(f'/root/mansura/logs/access/general/{current_date}.txt', 'a') as f:
                f.write(err_string)
        else:
            with open(f'/root/mansura/logs/access/user/{current_date}.txt', 'a') as f:
                f.write(err_string)
    elif msg_type == "distro":
        err_string = f"{log_string}"
        my_path = f"/root/mansura/logs/distro/{vote_type}/{current_date}"
        modules.check_and_save_dir(my_path)
        if distro_type == "initial":
            with open(f'{my_path}/FULL_SET.txt', 'a') as f:
                f.write(err_string + ",\n")
        else:
            with open(f'{my_path}/DISTRO.txt', 'a') as f:
                f.write(err_string + ",\n")
    elif msg_type == 'payment':
        my_path = f"/root/mansura/logs/payment"
        modules.check_and_save_dir(my_path)
        with open(f'{my_path}/{current_date}.txt', 'a') as f:
                f.write(err_string + ",\n")
    elif msg_type == 'test':
        my_path = f"/root/mansura/Python/logs/test"
        modules.check_and_save_dir(my_path)
        with open(f'{my_path}/{current_date}.txt', 'a') as f:
                f.write(err_string + ",\n")