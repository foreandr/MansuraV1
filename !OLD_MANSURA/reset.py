from Python.database import USER_FULL_RESET
def SERVER_RESET():
    # RESET WITHOUT DROPPING TABLES
    #check_server_side_reset = input('ARE YOU SURE YOU WANT TO SERVER SIDE RESET:\n')
    #if check_server_side_reset == "y".lower() or check_server_side_reset == "yes".lower():
    USER_FULL_RESET(server="true")

# RESET_DATABASE()
SERVER_RESET()