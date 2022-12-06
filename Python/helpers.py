import os.path
import random
import json

from os import path
import os
from nudenet import NudeClassifier # NUDITY CLASSIFIER


def CHECK_IF_MOBILE(request):
    devices = ["Android", "webOS", "iPhone", "iPad", "iPod", "BlackBerry", "IEMobile", "Opera Mini"]
    result = False
    try:
        if any (device in request.environ["HTTP_USER_AGENT"] for device in devices): 
            result = True 
        # print("REQUEST AGENT:", request.environ["HTTP_USER_AGENT"], result)
        return result
    except Exception as e:
        log_function("error", e)
        return result

def NLP_KEYWORD_EXTRACTOR(text):
    keywords = text.split(" ")

    # NOT GOING TO USE NLP
    '''
    import yake # NATURAL LANGUAGE PROCESSING
    kw_extractor = yake.KeywordExtractor()
    # text = """spaCy is an open-source software library for advanced natural language processing, written in the programming languages Python and Cython. The library is published under the MIT license and its main developers are Matthew Honnibal and Ines Montani, the founders of the software company Explosion."""
    language = "en"
    max_ngram_size = 3 # The max_ngram_size is limit the word count of the extracted keyword. If you keep max_ngram_size=3, then keyword length will not increase more than 3. But, It will also have keywords with a size less than 3.
    deduplication_threshold = 0.3 # 1 (no dupes) -> 9 (lots of dupes)
    numOfKeywords = 13
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(text)
    '''
    #print(type(keywords))
    #print(keywords)

    #list_of_keywords = []
    #for i in keywords:
    #    list_of_keywords.append(i[0])

    #for i in list_of_keywords:
    #    print(i)
    # print("POST KEYWORDS:", keywords)
    return keywords

NLP_KEYWORD_EXTRACTOR("""spaCy is an open-source software library for advanced natural language processing, 
written in the programming languages Python and Cython. The library is published under the MIT license
and its main developers are Matthew Honnibal and Ines Montani, the founders of the software company Explosion.""")

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

    post_text = ""
    post_age_18 = ""
    post_source = ""
    post_image_path = ""

    # TESTING IF THERE IS AN IMAGE
    pic_path = os.path.join(my_path + "/pic.jpg").strip()

    if not path.exists(pic_path):
        post_image_path = ""
    else:
        post_image_path = pic_path[7:]
    

    f = open(f'{my_path}/post_config.json')
    data = json.load(f)
    post_text = data["txt"]
    post_age_18 = data["18+"]
    post_sources = data["external_source"]
    distro_details = data["distro_details"]
    #print(post_text, post_age_18,  post_sources, post_image_path)
    #print(my_path)
    #print("TEXT:",post_text , len(post_text))
    #print("OV18:",post_age_18 , len(post_age_18))
    #print("SRC?:",post_sources , len(post_sources))
    #print("IMG-:",post_image_path , len(post_image_path))
    #print()
    return post_text, post_age_18, post_sources, post_image_path, distro_details


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


def USERNAME_PROFANITY_CHECK(word, testing=False): #todo: this is particular to username
    print("CHECKING USERNAME FOR BADWORDS: ", type(word), {word})
    
    if testing:
        f = open("bad_words_username.txt", "r")
    else:
        f = open("Python/bad_words_username.txt", "r")
        
    from better_profanity import profanity
 # print(word[0])
        
    # NO IDEA WTF IS GOING ON WITH THE LIST SHIT
    # word = word[0] #TODO: MUST BE ON 
    # print("word:", word)
    # BASIC CHECK IF == TO ANY
    bad_words = f.read().split(",")
    for i in bad_words:
        if i != "" and i != " ":
            if i in word:
                print(F"FOUND {i} in {word} {len(i)}")
                return True
            else:
                pass
                #print("NOT FOUND",i, {len(i)})
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
        print(f"{word} TOO LONG: {len(word)}")
        return True       
    
    #5 ALPHANUMERIC
    if any(not c.isalnum() for c in word):
        print(f"{word} has non alphanumeric chracters, cant in name")
        return True
    
    return False


def CHANGE_TO_JSON_FORMATTED(my_string):
    # ALL THIS ADHOC-CLEANING IS A NIGHTMARE, NEED A BETTER WAY

    #print(my_string)
    #print(my_string)
    #print()
    
    string_array = my_string.split(":")
    #print(string_array)
    #print()

    contents_of_clause = string_array[1]
    #print(contents_of_clause)
    #print()
    #print("contents_of_clause       :", contents_of_clause)
    contents_of_clause = contents_of_clause.replace("'AND", '"AND')
    contents_of_clause = contents_of_clause.replace("',", '",')
    #print(contents_of_clause)
    #print()
    #print("contents_of_clause       :", contents_of_clause)
    if contents_of_clause[0] == " ":
        contents_of_clause = '"' + contents_of_clause[2:-1] + '"'
    elif contents_of_clause[0] == "'":
        contents_of_clause = '"' + contents_of_clause[1:-1] + '"'
    
    final_content = string_array[0] + ":" + contents_of_clause
   
    # print("final_content",final_content)
    return final_content


def TURN_STRING_TO_DICT(my_string):
    # LOTS OF ARBITRARY SHIT IN HERE BUT IT WORKS...for now..
    #JSON FORMATTING IS TREMENDOUSLY ANNOYING
    # https://jsonlint.com/ # this is becomming the most disgusting piece of filt ive ever seen
    # print("OG CHECKER1",my_string) 

    #print(my_string)
    #print("changed")
    if type(my_string) == "Nonetypee" or my_string == "Nonee":
        my_json_dict = {"where_full_query":"",
        "order_by_clause":""}
        new_json = json.loads(my_json_dict, strict=False)
        return new_json

    if "now())::date" in my_string:
        # print("DOING THE REPLACE")
        my_string = my_string.replace(", now())::date", "*** now())::date")
        #print(my_string)
        #exit(0)'
    
    my_string_array = my_string.split(',')


    count = 0
    reconstructed_string = ""
    for i in my_string_array:
        #print(count, i)
        if count != 4 and count != 5:
            i = i.replace("'", '"')
        else:
            #print("BEFORE", i)
            if count == 4:
                #print(count, i, "UNCHANGED")
                # print(i)
                i = CHANGE_TO_JSON_FORMATTED(i)
                #print(count, i, "CHANGED")
            # print("AFTER", i)
        
        if count != 5:
            reconstructed_string += i + ","
        else:
            reconstructed_string += i

        count+=1

    reconstructed_string = reconstructed_string.replace("'where_full_query'",'"where_full_query"')
    reconstructed_string = reconstructed_string.replace("'order_by_clause'",'"order_by_clause"')

    #print("===========================")
    #print(reconstructed_string)
    #print("===========================")
    reconstructed_string = reconstructed_string.replace("***", ",")
    #print(reconstructed_string)
    #print("===========================")
    
    #print(reconstructed_string)
    new_json = json.loads(reconstructed_string, strict=False)
    #print("NEW JSON", new_json)
    # exit()
    return new_json


def GIANT_FILE_INSERT():
    f = open("names.txt", "r")
    Lines = f.readlines()
    
    count = 0
    
    with open('TEST_STRING_DEMO.txt', 'a') as f:
        f.write(F'\n\ndef GIANT_FILE_INSERT():\n')
    mylist = ["EQUAL DISTRIBUTION", "LOG DISTRIBUTION"]
    for line in Lines:
        count += 1
        # print("Line{}: {}".format(count, line.strip()))
        name = line.strip()
        my_string = (f"""\tDB.FILE_INSERT( uploader='{name}', uploaderId=DB.GET_USER_ID( '{name}'), size=100, post_foreign_id_source="{random.randint(1, count+1)}", file_path="N-A", post_file="", post_text="testing a string hello hello hello", age_18="older_18", external_link="",  distro_details=['{random.choice(mylist)}', 'None'])""")
        
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


def POST_TEXT_CHECK(entered_string):
    """
    f = open("/root/mansura/Python/bad_words_post.txt", "r")
    bad_words = f.read()
    print(F"bad words:\n{bad_words}")
    """


    from better_profanity import profanity
    censored_text = profanity.censor(entered_string)
    # print(censored_text)


    # print(len(text_list))
    #print(text_list)
    return censored_text


def POST_IMG_CHECK(image_file, testing=False):
    #PUT THIS IN THE MOUNTED DIR
    
    print("CHECK IMAGE FILE",image_file )
    if testing:
        target = rf'/root/mansura/Python/nude_test/{image_file.filename}'#TODO: DIFFERENTIATE DIFFERENT EXTENSIONS
    else:
        target = rf'/root/mansura/Python/nude_test/{image_file.filename}'#TODO: DIFFERENTIATE DIFFERENT EXTENSIONS
        image_file.stream.seek(0) #need this part in here so it doesnt give 0 bits in a later save
        image_file.save(target)
    

    # initialize classifier (downloads the checkpoint file automatically the first time)
    try:
        # target = "/root/mansura/Python/nude_test/0.042468_42220.jpg"
        classifier = NudeClassifier()
        
        # Classify single image
        var = (classifier.classify(target))
        safe_percent = (var[list(var)[0]]["safe"])
        unsafe_percent = (var[list(var)[0]]["unsafe"])

    
        if safe_percent > 0.65: #I MAY HAVE TO CHANGE THIS
            print(F"SAFE  :{safe_percent}")
            return True
        else:
            print(F"UNSAFE:{unsafe_percent}")
            return False
        # print(var)
    except Exception as e:
        #print(e)
        log_function("error", e)
        return False
    

def STRING_SIMILARITY_CHECK(a, b):
    from difflib import SequenceMatcher
    return SequenceMatcher(None, a, b).ratio()


def log_function(msg_type, log_string, vote_type="None", distro_type="None"):
    #if log_string == "write() argument must be str, not None":
    #    print("got here")
    #    return "" # THIS ERROR CAN BE IGNORED
    # print(f"TESTING:{log_string}")
    import csv
    from datetime import datetime
    import pytz

    my_time = pytz.timezone('US/Eastern') 
    current_datetime = datetime.now(my_time).replace(microsecond=0).replace(tzinfo=None)
    current_date = current_datetime.strftime('%Y-%m-%d')
    err_string = f"{current_datetime} [{msg_type}]- {log_string}\n" 

    if msg_type == "error":        
        print("==========LOGGING AN ERROR PLS NOTICE!=========")
        with open(f'/root/mansura/Python/logs/errors/{current_date}.txt', 'a') as f:
            f.write(err_string)
    elif msg_type == "request":
        with open(f'/root/mansura/Python/logs/access/{current_date}.txt', 'a') as f:
            f.write(err_string)
    elif msg_type == "distro":
        err_string = f"{log_string}"
        my_path = f"/root/mansura/Python/logs/distro/{vote_type}/{current_date}"
        check_and_save_dir(my_path)
        if distro_type == "initial":
            with open(f'{my_path}/FULL_SET.txt', 'a') as f:
                f.write(err_string + ",\n")
        else:
            with open(f'{my_path}/DISTRO.txt', 'a') as f:
                f.write(err_string + ",\n")
    elif msg_type == 'payment':
        my_path = f"/root/mansura/Python/logs/payment"
        with open(f'{my_path}/{current_date}.txt', 'a') as f:
                f.write(err_string + ",\n")


                

        

def remove_values_from_list(the_list):
   return [value for value in the_list if value != "None" or value != None ]


def GET_ALL_QUERY_INFO_FROM_REQUEST_FORM(request):
    and_or_clauses = []
    where_clauses = []
    hi_eq_low = []
    num_search_text = []
   
    
    and_or_clauses.append(request.form.get(f"and_or_clause"))
    where_clauses.append(request.form.get(f"where_clauses"))
    hi_eq_low.append(request.form.get(f"higher_equal_lower"))
    num_search_text.append(request.form.get(f"num_search_text"))

    for i in range(1, 10):
        and_or_clauses.append(request.form.get(f"and_or_clause{i}"))
        where_clauses.append(request.form.get(f"where_clauses{i}"))
        hi_eq_low.append(request.form.get(f"higher_equal_lower{i}"))
        num_search_text.append(request.form.get(f"num_search_text{i}"))
    
    # REMOVING EXTRAS
    #and_or_clauses = remove_values_from_list(and_or_clauses)
    #where_clauses = remove_values_from_list(where_clauses)
    #hi_eq_low = remove_values_from_list(hi_eq_low)
    #num_search_text = remove_values_from_list(num_search_text)
    final_and_or_clauses = []
    final_where_clauses = []
    final_hi_eq_low = []
    final_num_search_text = []

    for i in range(len(and_or_clauses)): # any would do
        temp_and_or_clauses = and_or_clauses[i]
        temp_where_clauses = where_clauses[i]
        temp_hi_eq_low = hi_eq_low[i]
        temp_num_search_text = num_search_text[i]
        
        if (temp_and_or_clauses != None) and (temp_where_clauses != None) and (temp_hi_eq_low != None) and ((temp_num_search_text != None) or (temp_num_search_text != "")):
            # print("temp_num_search_text", len(temp_num_search_text), temp_num_search_text)
            if temp_num_search_text != "":
                final_and_or_clauses.append(temp_and_or_clauses)
                final_where_clauses.append(temp_where_clauses)
                final_hi_eq_low.append(temp_hi_eq_low)
                final_num_search_text.append(temp_num_search_text)

    return final_and_or_clauses, final_where_clauses, final_hi_eq_low, final_num_search_text


def TURN_WHERE_CLAUSE_TO_STRING(query_list):
    # print("WHERE_CLAUSE_TO_STRING: ", query_list)
    
    if len(query_list) == 0:
        # print("empty list")
        return ""
    
    and_or = query_list[0]
    question =  query_list[1]
    comparison = query_list[2]
    amount = query_list[3]

    if comparison == "==":
        comparison = "="
    #print("and_or      :", and_or)
    #print("question    :", question)
    #print("comparison  :", comparison)
    #print("amount      :", amount)

    recomposed_string = ""
    print("QUESTION:", question)
    # THIS IS WHERE THE WHERE CLAUSES GET TRANSLATED INTO QUURIES, WILL EVENTUALLY BE TURNED INTO IT'S OWN FUNCTION
    if question == "POST DAY VOTES":
        question_string = "(SELECT COUNT(*) FROM FILE_VOTES file WHERE file.File_id = F.File_id AND Vote_Type = 'Daily')"
    elif question == "POST MONTH VOTES":
        question_string = "(SELECT COUNT(*) FROM FILE_VOTES file WHERE file.File_id = F.File_id AND Vote_Type = 'Monthly')"
    elif question == "POST YEAR VOTES":
        question_string = "(SELECT COUNT(*) FROM FILE_VOTES file WHERE file.File_id = F.File_id AND Vote_Type = 'Yearly')"
    else: #DEFAULT BECAUSE OF A BREAK, CLICKED AN OPTION NOT IMPLEMENTED IN WHERE CLAUSE
         question_string = ""
    
    recomposed_string += and_or + " "
    recomposed_string += question_string + " "
    recomposed_string += comparison + " "
    recomposed_string += amount + " "
    #print("ENTIRE RECOMPOSED STRING:")
    print("ANSWER:", recomposed_string)
    return recomposed_string


def SPLIT_AND_RECOMPOSE_ORDER_BY_CLAUSES(giant_order_string):
    order_by_sections = giant_order_string.split("ORDER BY")
    #print("==========CHECKING FOR DUPES===================")
    order_by_sections= list(dict.fromkeys(order_by_sections))
    new_order_by_string = "ORDER BY"
    for i in range(len(order_by_sections)):
        # print(i, len(order_by_sections[i]), order_by_sections[i])
        if len(order_by_sections[i]) > 1: # THIS SHOULD BE 0 THERE IS AN EXTRA SPACE CREATED SOMEWHERE IN THE CODE, so it has to be > 1
            new_order_by_string += order_by_sections[i] + ","

    #print(new_order_by_string)
    new_order_by_string = new_order_by_string[:-1]
    #print(new_order_by_string)
    return new_order_by_string
    

def COMPOSE_SEARCHARGS_AND_JSONCLAUSE(returned_search_arguments, json_search_clauses):
    # print("==============WITHIN COMPOSE SEARCH AND JSON==============")
    #print("returned_search_arguments:",type(returned_search_arguments), returned_search_arguments)
    #print("json_search_clauses      :",type(json_search_clauses), json_search_clauses)
    
    #TODO: WHAT I MIGHT HAVE TO DO IS GO TO THE SEARCH ALGO-PATH AS WELL AND CONTACT
    new_composed_where_clause = ""
    new_composed_order_by_clause = ""
    
    if str(returned_search_arguments) != "None":
        if type(returned_search_arguments) != dict:
            returned_search_arguments = eval(returned_search_arguments)
        new_composed_where_clause = str(returned_search_arguments['where_full_query']) + " " + str(json_search_clauses['WHERE_CLAUSE'])
        
        #print("\nnew_composed_where_clause:", new_composed_where_clause)
        #print("\nreturned_search_arguments['where_full_query']:", returned_search_arguments['where_full_query'])
        #print("\njson_search_clauses['WHERE_CLAUSE']:", json_search_clauses['WHERE_CLAUSE'])
    
    if str(json_search_clauses) != "None":
        if type(json_search_clauses) != dict:
            json_search_clauses = eval(json_search_clauses)
        # print("GOT HERE CHECKPOINT")
        #print(returned_search_arguments['order_by_clause'])
        #print(json_search_clauses['ORDER_BY_CLAUSE'])
        new_composed_order_by_clause = SPLIT_AND_RECOMPOSE_ORDER_BY_CLAUSES(returned_search_arguments['order_by_clause'] + json_search_clauses['ORDER_BY_CLAUSE'])
        #print("CHECK 1", returned_search_arguments['order_by_clause'])
        #print("CHECK 2", json_search_clauses['ORDER_BY_CLAUSE'])
        #print("CHECK 3", new_composed_order_by_clause)
        #print("new_composed_order_by_clause\n", new_composed_order_by_clause)
    
    #TODO: SOMETHING IN HERE TO DELETE ALL THE EXTRA TIMES IT SAYS AND USERNAME == USERNAME
    
    new_return_clause = {
        'WHERE_CLAUSE': new_composed_where_clause,
        'ORDER_BY_CLAUSE':new_composed_order_by_clause
    }
    return new_return_clause


def CHANGE_BIO(my_string, user):
    my_path = f"/root/mansura/static/#UserData/{user}/config.json"
    with open(my_path, "r") as jsonFile:
        data = json.load(jsonFile)
    data["bio"] = my_string
    with open(my_path, "w") as jsonFile:
        json.dump(data, jsonFile)

def CREATING_EMBED_STRUCTURE(link):
    print("ORIGIN", link)
    
    tiktok_template = '''                
        <blockquote class="tiktok-embed" cite="https://www.tiktok.com/@LOCATION_FOR_TIKTOK_UPLOADER_USERNAME/video/LOCATION_FOR_TIKTOK_UPLOADER_VIDEO_ID" data-video-id="LOCATION_FOR_TIKTOK_UPLOADER_VIDEO_ID" style="max-width: 605px;min-width: 325px;"> 
            <section> 
                <a href="https://www.tiktok.com/@LOCATION_FOR_TIKTOK_UPLOADER_USERNAME?refer=embed"></a>
            </section>
        </blockquote>
        <!--PROPERLY EMBEDDED HTML TAG-->
        '''
    if link == None:
        return link
    if "tiktok" in link:
        #print("THIS IS A TIKTOK VIDEO")
        
        #A TYPICAL LINK LOOKS LIKE THIS https://www.tiktok.com/@lucciamv1/video/7173015261623225642?is_copy_url=1&is_from_webapp=v1
        tiktok_list = link.split("https://www.tiktok.com/@")
        #print("tiktok_list", tiktok_list)
        
        tiktok_base_url = tiktok_list[1]
        #print("tiktok_base_url", tiktok_base_url)
        
        username_video_split = tiktok_list[1].split("/video/")
        username = username_video_split[0]
        #print("username", username)
        
        tiktok_video_file_id = username_video_split[1].split("?")[0] # this seems to be in the videos, i could imagine it leading to problems   
        #print("tiktok_video_file_id", tiktok_video_file_id)
        
        # REPLACE THE TEMPLATE
        tiktok_template = tiktok_template.replace("LOCATION_FOR_TIKTOK_UPLOADER_USERNAME", username)
        tiktok_template = tiktok_template.replace("LOCATION_FOR_TIKTOK_UPLOADER_VIDEO_ID", tiktok_video_file_id)
        
        link = tiktok_template
        
        #print(F"FINAL LINK", link)

    
    elif "youtube" in link:
        #print("THIS IS A YOUTUBE VIDEO")
        youtube_template = '''
        <iframe width="560" height="315" src="https://www.youtube.com/embed/YOUTUBE_FILE_ID" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
        </iframe>
        <!--PROPERLY EMBEDDED HTML TAG-->
        '''
        
        link_without_watch = link.split("watch?v=")
        #print("link_without_watch", link_without_watch)
        
        youtube_file_id = link_without_watch[1]
        #print("youtube_file_id", youtube_file_id)
        
        youtube_template = youtube_template.replace("YOUTUBE_FILE_ID", youtube_file_id)
        link = youtube_template

    print("FINAL", link)
    return link




#demo_list = ['AND', 'POST DAY VOTES', '==', '9']
#demo_list2 = ['OR', 'POST MONTH VOTES', '<=', '10']
#demo_list3 = ['AND', 'POST YEAR VOTES', '==', '1']
#TURN_WHERE_CLAUSE_TO_STRING(demo_list)
#TURN_WHERE_CLAUSE_TO_STRING(demo_list2)
#TURN_WHERE_CLAUSE_TO_STRING(demo_list3)

    
# GET_USER_BIO("foreandr")
# FULL_GIANT_REGISTER()
# print(USERNAME_sPROFANITY_CHECK("bozo0000000000000000", testing=True))
# print(get_postinfo_from_path("/root/mansura/static/#UserData/foreandr/files/foreandr-157"))

"/root/mansura/static/#UserData/foreandr/files/foreandr-157/pic.jpg"
"/root/mansura/static/#UserData/foreandr/files/foreandr-157/pic.jpg"
# POST_IMG_CHECK("test",testing=True)
# POST_IMG_CHECK("", True)
# POST_TEXT_CHECK("")