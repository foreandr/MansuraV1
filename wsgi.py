from mansura import *

if __name__ == "__main__":
    #my_port = 443
    host = "0.0.0.0" #could be local host
    # logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.DEBUG) #ISN'T    WORKING THE WAY I WANT
    # database.USER_FULL_RESET()
    
    thread = Thread(target = distribution_algorithm.TESTING_TIMING, args = ())
    thread.start()

    app.run(host=host, port="8080", debug=True, use_reloader=False)  # host is to get off localhost