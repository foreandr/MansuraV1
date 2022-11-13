import csv
from datetime import datetime
import pytz

def write_to_log_daily_log_file(msg_type, log_string):
    my_time = pytz.timezone('US/Eastern') 
    current_datetime = datetime.now(my_time).replace(microsecond=0).replace(tzinfo=None)
    current_date = current_datetime.strftime('%Y-%m-%d')
    err_string = f"{current_datetime} [{msg_type}]- {log_string}\n" 
    
    if msg_type == "error":        
        with open(f'logs/errors/{current_date}.txt', 'a') as f:
            f.write(err_string)

    elif msg_type == "request":
        with open(f'logs/access/{current_date}.txt', 'a') as f:
            f.write(err_string)

write_to_log_daily_log_file("error", "hello world")        
write_to_log_daily_log_file("request", "hello world")
write_to_log_daily_log_file("error", "hello world")