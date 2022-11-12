import os.path
import random
import json

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


def get_postinfo_from_path(my_path):
    from os import path
    post_text = ""
    post_age_18 = ""
    post_source = ""
    post_image_path = ""

    # TESTING IF THERE IS AN IMAGE
    pic_path = my_path + "/pic.jpg"
    if not path.exists(pic_path):
        post_image_path = ""

    for filename in os.listdir(my_path):
        f = os.path.join(my_path, filename)

        if os.path.isfile(f):
            x = open(f, "r")
             # check which file it is
            if "age_18" in f:                     
                post_age_18 = x.read()
            elif "source" in f: 
                post_sources = x.read()
            elif "post_text" in f:                    
                post_text = x.read()
            elif "pic" in f:
                post_image_path = pic_path[7:] # remove static

    #print(post_text, post_age_18,  post_sources, post_image_path)
    #print(my_path)
    #print("TEXT:",post_text , len(post_text))
    #print("OV18:",post_age_18 , len(post_age_18))
    #print("SRC?:",post_sources , len(post_sources))
    #print("IMG-:",post_image_path , len(post_image_path))
    #print()
    return post_text, post_age_18,  post_sources, post_image_path


def print_model_details(ids, paths, descriptions, dates, id1, uploaders, ids1, paths1, sizes, id2, date,
                        votes):
    print('======================ALL MODEL DETAILS FOR FILE====================')
    print(ids)
    print(paths)
    print(descriptions)
    print(dates)
    print(id1)
    print(uploaders)
    print(ids1)
    print(paths1)
    print(sizes)
    print(id2)
    print(date)
    print(votes)

    print('=====================================================================')


def print_green(string):
    print(bcolors.OKGREEN + str(string) + bcolors.ENDC)


def print_title(string):
    print(bcolors.HEADER + bcolors.UNDERLINE + str(string) + bcolors.ENDC)


def print_error(string):
    print(bcolors.FAIL + str(string) + bcolors.ENDC)


def print_warning(string):
    print(bcolors.WARNING + str(string) + bcolors.ENDC)


def save_to_file(filename="demofile"):
    save_path = 'GraphTheory'
    completeName = os.path.join(save_path, filename + ".csv")


def turn_pic_to_hex(filepath="../#UserData/userpic.jpg"):
    with open(filepath, 'rb') as f:
        content = f.read()
    return content


def check_and_save_dir(path):
    isExist = os.path.exists(path)
    # print(isExist)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
        # print("The new directory is created:", path)


def turn_hex_to_pic_save(hex_string, username="DEMO-USERNAME"):
    import binascii
    # my_ascii = (binascii.hexlify(hex_string))
    with open(F'../#DemoData/{username}-image.jpg', 'wb') as file:
        file.write(hex_string)


def get_filetype(string):
    txt = string[::-1]
    my_text = txt.split(".")[0]
    return my_text[::-1]


def check_no_bad_words(word, testing=False): #todo: this is particular to username
    print("CHECKING USERNAME FOR BADWORDS: ", type(word), {word})
    
    if testing:
        f = open("bad_words.txt", "r")
    else:
        f = open("Python/bad_words.txt", "r")
        
    from better_profanity import profanity
 # print(word[0])
        
    # NO IDEA WTF IS GOING ON WITH THE LIST SHIT
    # word = word[0] #TODO: MUST BE ON 
    # print("word:", word)
    # BASIC CHECK IF == TO ANY
    bad_words = f.read().split(",")

    # 1. my word check
    if word.lower() in bad_words:
        print("it is in list of bad words")
        return True
        
    # 2. simple profanity check
    if profanity.contains_profanity(word):
        print("DETECTED BY PROFTANITY LIBRARY")
        return True
        
    # 3. spaces check
    if ' ' in word:
        print("THERE IS A SPACE IN ", word)
        return True
        
    # 4: 20 CHARS
    if len(word) > 20:
        print(word, "TOO LONG")
        return True       
    
    return False


def GIANT_FILE_INSERT():
    f = open("names.txt", "r")
    Lines = f.readlines()
    
    count = 0
    
    with open('TEST_STRING_DEMO.txt', 'a') as f:
        f.write(F'\n\ndef GIANT_FILE_INSERT():\n')

    for line in Lines:
        count += 1
        # print("Line{}: {}".format(count, line.strip()))
        name = line.strip()
        my_string = (f"""\tDB.FILE_INSERT( uploader='{name}', uploaderId=DB.GET_USER_ID( '{name}'), size=100, post_foreign_id_source="{random.randint(1,300)}", file_path="N-A", post_file="", post_text="testing a string hello hello hello", age_18="older_18", external_link="")""")
        with open('TEST_STRING_DEMO.txt', 'a') as f:
            f.write(F'{my_string}\n')


def GIANT_USER_REGISTER():
    f = open("names.txt", "r")
    Lines = f.readlines()
    
    count = 0
    
    with open('TEST_STRING_DEMO.txt', 'a') as f:
        f.write(F'\n\ndef GIANT_USER_REGISTER():\n')

    for line in Lines:
        count += 1
        # print("Line{}: {}".format(count, line.strip()))
        name = line.strip()
        my_string = (f"""\tDB.full_register('{name}', 'password', '{name}@gmail.com', '{name}@gmail.com', 5)""")
        
        with open('TEST_STRING_DEMO.txt', 'a') as f:
            f.write(F'{my_string}\n')


def GIANT_FILE_VOTE_INSERT():
    f = open("names.txt", "r")
    Lines = f.readlines()
    
    count = 0
    
    with open('TEST_STRING_DEMO.txt', 'a') as f:
        f.write(F'\n\ndef GIANT_FILE_VOTE_INSERT():\n')

    for line in Lines:
        count += 1
        # print("Line{}: {}".format(count, line.strip()))
        name = line.strip()
        my_string = (f"""\tDB.FILE_VOTE_INSERT( '{name}', {random.randint(1,300)},  'Daily')\n\tDB.FILE_VOTE_INSERT( '{name}', {random.randint(1,300)},  'Monthly')\n\tDB.FILE_VOTE_INSERT( '{name}', {random.randint(1,300)},  'Yearly')""")
        
        with open('TEST_STRING_DEMO.txt', 'a') as f:
            f.write(F'{my_string}\n')


def GIANT_USER_SUBSCRIBE():
    f = open("names.txt", "r")
    Lines = f.readlines()
    
    count = 0
    
    with open('TEST_STRING_DEMO.txt', 'a') as f:
        f.write(F'\n\ndef GIANT_SUBSCRIBE():\n')

    for line in Lines:
        count += 1
        # print("Line{}: {}".format(count, line.strip()))
        name = line.strip()
        my_string = (f"""\tDB.MANSURA_SUBSCRIBE('{name}')""")
        
        with open('TEST_STRING_DEMO.txt', 'a') as f:
            f.write(F'{my_string}\n')


def FULL_GIANT_REGISTER():
    
    # GET RID OF EVERYTHING INSIDE
    with open("TEST_STRING_DEMO.txt",'r+') as f:
        f.truncate(0)

    # PUT THE STUFF INSIDE
    my_string = "import Python.database as DB"
    with open('TEST_STRING_DEMO.txt', 'a') as f:
        f.write(F'{my_string}')

    GIANT_FILE_INSERT()
    GIANT_USER_REGISTER()
    GIANT_FILE_VOTE_INSERT()
    GIANT_USER_SUBSCRIBE()

def GET_USER_BIO(username):
    f = open(f'/root/mansura/static/#UserData/{username}/config.json')
    data = json.load(f)
    # print(type(data), data)
    my_bio = data["bio"]
    f.close()
    return my_bio

# GET_USER_BIO("foreandr")
# FULL_GIANT_REGISTER()