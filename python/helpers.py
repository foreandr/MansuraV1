import os as os

def check_and_save_dir(path):
    # Create a new directory because it does not exist
    print("RUNNING CHECK AND SAVE DIR")
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_green(string):
    print(bcolors.OKGREEN + str(string) + bcolors.ENDC)


def print_title(string):
    print(bcolors.HEADER + bcolors.UNDERLINE + str(string) + bcolors.ENDC)


def print_error(string):
    print(bcolors.FAIL + str(string) + bcolors.ENDC)


def print_warning(string):
    print(bcolors.WARNING + str(string) + bcolors.ENDC)        