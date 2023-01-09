import os as os
import inspect
from os import listdir
from PIL import Image as PImage
from better_profanity import profanity
import hashlib
import datetime

try:    
    import python.MODULES as modules
except:
    import MODULES as modules

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

def validate_user_from_session(email, password):
    try:
        cursor, conn = modules.create_connection()
        # print(f"VALIDATE {email} | {password}")  # GET THIS FROM JAVASCRIPT
        cursor.execute(f"""
        SELECT * 
        FROM USERS
        WHERE email = %(email)s
        AND password = %(password)s
        """, {'email': email,
            'password':hashlib.sha256(password.encode('utf-8')).hexdigest()}
        )
        tables = cursor.fetchall()
        user = ""
        user_id = ""
        for i in tables:
            # print(i)
            user_id = i[0]
            user = i[1]
            
        modules.close_conn(cursor, conn)
        
        if len(tables) > 0:
            print("SIGNING IN")
            return [True, user_id, user, email]
        else:
            print("NOT SIGNING IN")
            return [False]
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
def STRING_SIMILARITY_CHECK(a, b):
    from difflib import SequenceMatcher
    return SequenceMatcher(None, a, b).ratio()

def check_and_save_dir(path):
    # Create a new directory because it does not exist
    # print("RUNNING CHECK AND SAVE DIR")
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)

def print_segment():
    print("==============================")
    
def print_green(string):
    print(bcolors.OKGREEN + str(string) + bcolors.ENDC)

def print_title(string):
    print(bcolors.HEADER + bcolors.UNDERLINE + str(string) + bcolors.ENDC)

def print_error(string):
    print(bcolors.FAIL + str(string) + bcolors.ENDC)

def print_warning(string):
    print(bcolors.WARNING + str(string) + bcolors.ENDC)     
    
def remove_special_characters(string):
    return string

def check_tribunal_cuss_words(string):
    return string

def clean_title(Post_title):
    Post_title = remove_special_characters(Post_title)
    Post_title = check_tribunal_cuss_words(Post_title)
    
    return Post_title 

def clean_description(Post_description):
    return Post_description

def load_default_profile_pic():
    #img = PImage.open(path)
    #return img
    path = "/root/mansura/files/profile_demo.jpg"
    pic = open(path, 'rb').read()

    return pic
   
def USERNAME_PROFANITY_CHECK(word):
    # print("CHECKING USERNAME FOR BADWORDS: ", type(word), {word})

    f = open("/root/mansura/files/bad_words_username.txt", "r")        
    bad_words = f.read().split(",")
    for i in bad_words:
        if i != "" and i != " ":
            if i in word:
                print(F"FOUND {i} in {word} {len(i)}")
                return False
            else:
                pass

    # 1. my word check
    if word.lower() in bad_words:
        print("it is in list of bad words")
        return False
        
    # 2. simple profanity check
    if profanity.contains_profanity(word):
        print("DETECTED BY PROFTANITY LIBRARY")
        return False
        
    # 3. spaces check
    if ' ' in word:
        print("THERE IS A SPACE IN ", word)
        return False
        
    # 4: 20 CHARS
    if len(word) > 20:
        print(f"{word} TOO LONG: {len(word)}")
        return False      
    
    #5 ALPHANUMERIC
    if any(not c.isalnum() for c in word):
        print(f"{word} has non alphanumeric chracters, cant in name")
        return False
    
    return True

def triple_split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def SERVER_CHECK(server, function):
    try:
        cursor, conn = modules.create_connection()
        if server == "false":
            if function == "CREATE_TABLE_USER":
                cursor.execute("""DROP TABLE IF EXISTS USERS CASCADE""")
                modules.print_segment()
            
            elif function == "CREATE_TABLE_PEOPLE":
                cursor.execute("""DROP TABLE IF EXISTS PEOPLE CASCADE""")
                modules.print_segment()
            
            elif function == "CREATE_TABLE_POST":
                cursor.execute("""DROP TABLE IF EXISTS POSTS CASCADE""")
                modules.print_segment()
            
            elif function == "CREATE_TABLE_SUBJECTS":
                cursor.execute("""DROP TABLE IF EXISTS SUBJECTS CASCADE""")
                modules.print_segment()
            
            elif function == "CREATE_TABLE_LIKES":
                cursor.execute("""DROP TABLE IF EXISTS LIKES CASCADE""")
                modules.print_segment()
            
            elif function == "CREATE_TABLE_DISLIKES":
                cursor.execute("""DROP TABLE IF EXISTS DISLIKES CASCADE""")
                modules.print_segment()
            
            elif function == "CREATE_TABLE_COMMENTS":
                cursor.execute("""DROP TABLE IF EXISTS COMMENTS CASCADE""")
                modules.print_segment()
            
            elif function == "CREATE_TABLE_VIEWS":
                cursor.execute("""DROP TABLE IF EXISTS VIEWS CASCADE""")
                modules.print_segment()
            
            elif function == "CREATE_TABLE_CONNECTIONS":
                cursor.execute("""DROP TABLE IF EXISTS CONNECTIONS CASCADE""")
                modules.print_segment()
            
            elif function == "CREATE_TABLE_IP_ADRESSES":
                cursor.execute("""DROP TABLE IF EXISTS IP_ADRESSES CASCADE""")
                modules.print_segment()
                
            elif function == "CREATE_TABLE_CHAT_ROOMS":
                cursor.execute("""DROP TABLE IF EXISTS CHAT_ROOMS CASCADE""")
                modules.print_segment()
            
            elif function == "CREATE_TABLE_CHAT_ADMINS":
                cursor.execute("""DROP TABLE IF EXISTS CHAT_ADMINS CASCADE""")
                modules.print_segment()
            
            elif function == "CREATE_TABLE_POST_PERSON":
                cursor.execute("""DROP TABLE IF EXISTS POST_PERSON CASCADE""")
                modules.print_segment()
            
            elif function == "CREATE_TABLE_FAVOURITES":
                cursor.execute("""DROP TABLE IF EXISTS FAVOURITES CASCADE""")
                modules.print_segment()
                
            elif function == "CREATE_TABLE_CHAT_USERS":
                cursor.execute("""DROP TABLE IF EXISTS CHAT_USERS CASCADE""")
                modules.print_segment()
                
            elif function == "CREATE_TABLE_BLOCKS":
                cursor.execute("""DROP TABLE IF EXISTS BLOCKS CASCADE""")
                modules.print_segment()
                
            elif function == "CREATE_TABLE_REQUESTS":
                cursor.execute("""DROP TABLE IF EXISTS REQUESTS CASCADE""")
                modules.print_segment()
            
            elif function == "CREATE_TABLE_SUBJECT_REQUESTS":
                cursor.execute("""DROP TABLE IF EXISTS SUBJECT_REQUESTS CASCADE""")
                modules.print_segment()
                
            elif function == "CREATE_TABLE_1_TIME_PASSWORDS":
                cursor.execute("""DROP TABLE IF EXISTS ONE_TIME_PASSWORDS CASCADE""")
                modules.print_segment()
            
            elif function == "CREATE_TABLE_TRIBUNAL_WORD":
                cursor.execute("""DROP TABLE IF EXISTS TRIBUNAL_WORD CASCADE""")
                modules.print_segment()
            
            elif function == "CREATE_TABLE_TRIBUNAL_WORD_VOTE":
                cursor.execute("""DROP TABLE IF EXISTS TRIBUNAL_WORD_VOTE CASCADE""")
                modules.print_segment()
            
            elif function == "CREATE_TABLE_COMMENT_VOTES":
                cursor.execute("""DROP TABLE IF EXISTS COMMENT_VOTES CASCADE""")
                modules.print_segment()
                
            elif function == "CREATE_TABLE_MODERATION_ADMINS":
                cursor.execute("""DROP TABLE IF EXISTS MODERATION_ADMINS CASCADE""")
                modules.print_segment()
            
            elif function == "CREATE_TABLE_SEARCH_ALGORITHMS":
                cursor.execute("""DROP TABLE IF EXISTS SEARCH_ALGORITHMS CASCADE""")
                modules.print_segment()
                
            elif function == "CREATE_TABLE_SEARCH_ALGORITM_VOTES":
                cursor.execute("""DROP TABLE IF EXISTS SEARCH_ALGORITM_VOTES CASCADE""")
                modules.print_segment()
                
            elif function == "CREATE_TABLE_CURRENT_USER_SEARCH_ALGORITHM":
                cursor.execute("""DROP TABLE IF EXISTS CURRENT_USER_SEARCH_ALGORITHM CASCADE""")
                modules.print_segment()
                
            elif function == "CREATE_TABLE_SEARCH_ALGORITM_SAVE":
                cursor.execute("""DROP TABLE IF EXISTS SEARCH_ALGORITM_SAVE CASCADE""")
                modules.print_segment()             
        
            elif function == "CREATE_TABLE_POST_SUBJECTS":
                cursor.execute("""DROP TABLE IF EXISTS POST_SUBJECTS CASCADE""")
                modules.print_segment()    
                
            elif function == "CREATE_TABLE_USER_STATUS":
                cursor.execute("""DROP TABLE IF EXISTS USER_STATUS CASCADE""")
                modules.print_segment()  
                
            elif function == "CREATE_TABLE_CHAT_MESSAGES":
                cursor.execute("""DROP TABLE IF EXISTS CHAT_MESSAGES CASCADE""")
                modules.print_segment()  
        
            elif function == "CREATE_TABLE_CHAT_ROOM_INVITES":
                cursor.execute("""DROP TABLE IF EXISTS CHAT_ROOM_INVITES CASCADE""")
                modules.print_segment()  


            conn.commit()
            modules.print_green(F"CASCADE DROPPED TABLE {function}")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

def CHECK_IF_IT_IS_ME(id):
    if str(id) == "1":
        return "True"
    else:
        return "False" 
        
def CHECK_IF_MOBILE(request):
    devices = ["Android", "webOS", "iPhone", "iPad", "iPod", "BlackBerry", "IEMobile", "Opera Mini"]
    result = False
    try:
        if any (device in request.environ["HTTP_USER_AGENT"] for device in devices): 
            result = True 
        # print("REQUEST AGENT:", request.environ["HTTP_USER_AGENT"], result)
        return result
    except Exception as e:
        modules.log_function("error", e)
        return result
    
def CHECK_COMMENT_LIKE_EXISTS(Comment_id, User_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT COUNT(*)
            FROM COMMENT_VOTES
            WHERE Comment_id = %(Comment_id)s
            AND User_id = %(User_id)s          
        """, {'Comment_id':Comment_id,
            'User_id': User_id
            }
        )
        result = 0
        for i in cursor.fetchall():
            result = i[0]
        
        modules.close_conn(cursor, conn) 
        if result > 0:
            return True
        else: 
            return False
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
def CHECK_LIKE_EXISTS(Post_id, User_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT COUNT(*)
            FROM LIKES
            WHERE Post_id = %(Post_id)s
            AND User_id = %(User_id)s          
        """, {'Post_id': Post_id,
            'User_id': User_id
            }
        )
        result = 0
        for i in cursor.fetchall():
            result = i[0]
        
        modules.close_conn(cursor, conn) 
        if result > 0:
            return True
        else: 
            return False
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
def CHECK_CONNECTION_EXISTS(User_id1, User_id2):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT COUNT(*)
            FROM CONNECTIONS
            WHERE User_id1= %(User_id1)s
            AND User_id2 = %(User_id2)s          
        """, {'User_id1': User_id1,
            'User_id2': User_id2
            }
        )
        result = 0
        for i in cursor.fetchall():
            result = i[0]
        
        modules.close_conn(cursor, conn) 
        if result > 0:
            return True
        else: 
            return False    
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
       
def CHECK_FAVE_EXISTS(Post_id, User_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT COUNT(*)
            FROM FAVOURITES
            WHERE Post_id = %(Post_id)s
            AND User_id = %(User_id)s            
        """, {'Post_id': Post_id,
            'User_id': User_id
            })
        result = 0
        for i in cursor.fetchall():
            result = i[0]
        
        modules.close_conn(cursor, conn) 
        if result > 0:
            return True
        else: 
            return False
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
def CHECK_SEARCH_FAVE_EXISTS(Search_algorithm_id, User_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT COUNT(*)
            FROM SEARCH_ALGORITM_SAVE
            WHERE Search_algorithm_id = %(Search_algorithm_id)s
            AND User_id = %(User_id)s            
        """, {'Search_algorithm_id': Search_algorithm_id,
            'User_id': User_id
            })
        result = 0
        for i in cursor.fetchall():
            # print(Search_algorithm_id, User_id, i[0])
            result = i[0]
        
        modules.close_conn(cursor, conn) 
        if result > 0:
            return True
        else: 
            return False
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

def JANKY_COMMENT_CHECK(how_many):
    if how_many == str(11): # JANKY BUT SHOUDL WORK
        commenting =  "true"
    else:
        commenting =  "false"
    return commenting
 
def TRANSFRM_COMMENT_ARRAY_INTO_HTML(comment_array):
    html_array = []
    html_template = """
        <div>
            <div style="display: inline-block;">
                <h5>@USERNAME</h5> <h6>@DATE</h6>
            </div>
            
            <div style="word-break: break-all;"> <!--PREVENTS WRAP ARROUND-->
                <h6>@TEXT</h6>
            </div>

            <span>
                <button class="btn btn-outline-dark btn-lg" hx-post="/update_comment_like/@COMMENT_ID" hx-trigger="click" onclick="like_logic(this)">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-up-fill" viewBox="0 0 16 16">
                        <path d="m7.247 4.86-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z"/>
                    </svg>
                    <span id="comment_like_location@COMMENT_ID">
                    @NUM_COMMENT_VOTES
                    </span>
                </button>

            </span>
            
            <!--
            <span>
                <button class="btn" disabled>
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-down-fill" viewBox="0 0 16 16">
                        <path d="M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"/>
                    </svg>
                </button>
            </span> 
            -->
            
            <span>
                <button class="btn" disabled>
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chat-square-text" viewBox="0 0 16 16">
                    <path d="M14 1a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1h-2.5a2 2 0 0 0-1.6.8L8 14.333 6.1 11.8a2 2 0 0 0-1.6-.8H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2.5a1 1 0 0 1 .8.4l1.9 2.533a1 1 0 0 0 1.6 0l1.9-2.533a1 1 0 0 1 .8-.4H14a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/>
                    <path d="M3 3.5a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1-.5-.5zM3 6a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9A.5.5 0 0 1 3 6zm0 2.5a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5z"/>
                    </svg>
                </button>
            </span>
            
            <div>
            </br>
        </div>   
    """
    for i in comment_array:
        print(i)
        username = i[0]
        text = i[1]
        date = i[2]
        post_id = i[3]
        comment_id = i[4]
        
        num_comment_votes = modules.GET_NUM_COMMENT_VOTES_BY_ID(comment_id)
        print("username", username)
        print("text", text)
        print("date", date)
        print("post_id", post_id)
        print("comment_id", comment_id)
        print("num_comment_votes", num_comment_votes)
        
        temp_html = html_template.replace("@USERNAME", username)
        temp_html = temp_html.replace("@TEXT", text)
        temp_html = temp_html.replace("@COMMENT_ID", str(comment_id))
        temp_html = temp_html.replace("@NUM_COMMENT_VOTES", str(num_comment_votes))
        temp_html = temp_html.replace("@DATE", str((date.strftime('%Y-%m-%d'))))
        html_array.append(temp_html)
    
    return html_array

def GET_DOWNVOTES_BY_WORD(word):
    """ WAS GOING TO DO IT IN THE SQL BUT KEPT RUNNING INTO ISSUES
    down_votes = '''(SELECT COUNT(*) FROM TRIBUNAL_WORD_VOTE votes WHERE Vote_type = 'DOWN' )'''
    up_votes = '''(SELECT COUNT(*) FROM TRIBUNAL_WORD_VOTE votes WHERE Vote_type = 'UP' )'''    
    vote_count_check = f'''({down_votes} / ({down_votes} + {up_votes})) >= 0.0 '''       
    """
    try:
        cursor, conn = modules.create_connection()
        # GET DOWNVOTES    
        cursor.execute(f"""
            SELECT COUNT(*) 
            FROM TRIBUNAL_WORD_VOTE votes 
                    
            INNER JOIN TRIBUNAL_WORD word   
            ON word.Tribunal_word_id = votes.Tribunal_word_id
                    
            WHERE Vote_type = 'DOWN' 
            AND word.Tribunal_word =  %(word)s  
                """, {'word': word})
        downvotes = 0
        for k in cursor.fetchall():
            downvotes = k[0]     
        modules.close_conn(cursor, conn)
        return downvotes  
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
def GET_UPVOTES_BY_WORD(word):
    try:
        cursor, conn = modules.create_connection()
            # GET UPVOTES
        cursor.execute(f"""
                    SELECT COUNT(*) 
                    FROM TRIBUNAL_WORD_VOTE votes 
                    
                    INNER JOIN TRIBUNAL_WORD word   
                    ON word.Tribunal_word_id = votes.Tribunal_word_id
                    
                    WHERE Vote_type = 'UP' 
                    AND word.Tribunal_word = %(word)s
                            
        """, {'word': word}
        )
        upvotes = 0
        for j in cursor.fetchall():
            upvotes = j[0]   
        
        modules.close_conn(cursor, conn)
        return upvotes
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

def COMMENT_TEXT_CHECK(entered_string):
    try:
        cursor, conn = modules.create_connection()
        my_lines = []
        with open('/root/mansura/files/profanity_list.txt') as f:
            # print("opened fie")
            lines = f.readlines()[0].split(",") # NOT SURE WHY I HAVE TO INDEX FIRST
            my_lines = lines
            
        entered_string = entered_string.split(" ") # GET each word
            
        for i in range(len(entered_string)):
            # TOO STRICT
            #if not CHECK_INJECTION(entered_string[i]):
            #    entered_string[i] = "****"

            upvotes = GET_UPVOTES_BY_WORD(entered_string[i])
            downvotes = GET_DOWNVOTES_BY_WORD(entered_string[i])
                
            #print("UPVOTES      :", upvotes)
            #print("DOWNVOTES    :", downvotes)
                
            total_votes = int(upvotes) + int(downvotes)
            if downvotes >= 10:
                dislike_ratio = int(downvotes) / (total_votes)
                # print("dislike_ratio:",dislike_ratio)
                if (dislike_ratio) >= 0.8:
                    # print("changing", entered_string[i], "to ****")
                    entered_string[i] = "****"
                    
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

    modules.close_conn(cursor, conn) 
    final_string = " ".join((map(str,entered_string))) # turn list back to stirng
    return final_string
    
def COUNT_HOW_MANY_CUSS_WORD():
    try:
        cursor, conn = modules.create_connection()
        cursor.execute("""
        SELECT COUNT(*)
        FROM TRIBUNAL_WORD             
        """)
        
        for i in cursor.fetchall():
            print(i)
        modules.close_conn(cursor, conn)
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
def CHECK_POST_IS_LIVE(Post_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
        SELECT Post_live
        FROM POSTS    
        WHERE Post_id = '{Post_id}'
        """)
        results = ""
        for i in cursor.fetchall():
            results = i[0]
        modules.close_conn(cursor, conn)
        if results.lower() == "True".lower():
            return True
        else:
            return False
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

def GET_INJECTION_TERMS():
    f = open("/root/mansura/files/bad_words_username.txt", "r")
    injection_terms = f.read().split(",")
    injection_terms = list(map(lambda x: x.lower(), injection_terms))
    return injection_terms

def CHECK_USER_IS_GLOBAL_ADMIN(user_id):
    if user_id == 1:
        return "true"
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
        SELECT COUNT(*)
        FROM MODERATION_ADMINS
        WHERE User_id = '{user_id}'
        """)
        admin_exists = 0
        for i in cursor.fetchall():
            admin_exists = i[0]
        modules.close_conn(cursor, conn)
        if admin_exists == 0:
            # print("USER IS NOT ADMIN")
            return "false"
        else:
            # print("USER IS ADMIN")
            return "true"
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
 
def CHECK_INJECTION(word):
    array = modules.GET_INJECTION_TERMS()
    # print(array)
    if word.lower() in array:
        print(f"{word} is in {array}, not logging in")
        return False
    else:
        return True
       
def translate_link_to_html(link):
    #print("ORIGIN", link)
    changed = False
    if link == None:
        return link, changed
    try:
        if "tiktok" in link:
            # print("TIKTOKING")
            tiktok_template = '''<blockquote class="tiktok-embed" cite="https://www.tiktok.com/@LOCATION_FOR_TIKTOK_UPLOADER_USERNAME/video/LOCATION_FOR_TIKTOK_UPLOADER_VIDEO_ID" data-video-id="LOCATION_FOR_TIKTOK_UPLOADER_VIDEO_ID" style="max-width: 605px;min-width: 325px;" > <section> <a target="_blank" title="@LOCATION_FOR_TIKTOK_UPLOADER_USERNAME" href="https://www.tiktok.com/@LOCATION_FOR_TIKTOK_UPLOADER_USERNAME?refer=embed">@LOCATION_FOR_TIKTOK_UPLOADER_USERNAME</a></section></blockquote><script async src="https://www.tiktok.com/embed.js"></script>'''
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
            changed = True
            
        elif "youtube" in link:
            if "list" in link: # check if if it's a playlist or any other ways youtube can be fucked about with
                return link
            
            #print("THIS IS A YOUTUBE VIDEO")
            youtube_template = '''<iframe class="youtube-player" width="480" height="315" src="https://www.youtube.com/embed/YOUTUBE_FILE_ID" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'''
            
            link_without_watch = link.split("watch?v=")
            #print("link_without_watch", link_without_watch)
            
            youtube_file_id = link_without_watch[1].split("=")[0]
            #print("youtube_file_id 1 ", youtube_file_id)
            
            youtube_file_id = youtube_file_id.split("&")[0]
            #print("youtube_file_id 2 ", youtube_file_id)
            
            youtube_template = youtube_template.replace("YOUTUBE_FILE_ID", youtube_file_id)
            link = youtube_template
            changed = True

        elif "spotify" in link:
            # print(link, "\n")
                        
            spotify_template = """
                <iframe class="youtube-player" src="https://open.spotify.com/embed/episode/@SPOTIFY_EPISDE_ID?utm_source=generator" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
            """
            # https://open.spotify.com/episode/4CESb99rKgkQ5MvNL4HaFJ?si=3e1ea553d7c14637
            link_without_tail = link.split("?")[0]
            id = link_without_tail.split("episode/")[1]
            
            #print("SPOTIFY ID", id, "\n")
            
            spotify_template = spotify_template.replace("@SPOTIFY_EPISDE_ID", id)
            
            #print(spotify_template)
            link = spotify_template
            changed = True
        
        elif "rumble" in link:
            # TEMPLATE RUMBLE <iframe class="youtube-player" width="500" height="315" src="https://rumble.com/embed/v20cira/?pub=4" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
            link = link
        # print("NEW LINK:", link)
        return link,changed
    except Exception as e:
        modules.log_function("error", str(e), function_name=F"{inspect.stack()[0][3]}")
        return link,changed  

def translate_RUBMLE_LINK(embed_link):
    template = '''<iframe class="youtube-player" width="500" height="315" src="LINK_LOCATION" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'''
    template = template.replace("LINK_LOCATION", embed_link)
    return template

def TRANSLATE_SEARCH_RESULTS_TO_STATIC_HTML(results):
    print(results)

def GETTING_POST_MAX_FROM_QUERY(query):
    query = query.split("FROM POSTS posts")[1]
    select_portion = "SELECT COUNT(*) FROM POSTS posts"
    query = query.split("ORDER")[0]
    
    
    new_full_query = select_portion + query
    cursor, conn = modules.create_connection()
    cursor.execute(new_full_query)
    
    num_total = 0
    for i in cursor.fetchall():
        num_total = i[0]
    
    modules.close_conn(cursor, conn)
    return num_total

def CHECK_ALGO_FUNCTION(algo_name, user):
    #print("checking", algo_name)
    #print(algo_name, user)
    
    # 0  INJECTION CHECK
    if not modules.CHECK_INJECTION(algo_name):
        return "False"
    
    # 2. SPECIAL CHARACTERS  
    if any(not c.isalnum() for c in algo_name):
        # print(f"{algo_name} has non alphanumeric chracters, cant in name")
        return "False"  
     
    # 3. CHECK LENGTH
    if len(algo_name) > 20:
        # print(f"{algo_name} TOO LONG: {len(algo_name)}")
        return "False"    
    
    # 4 CHECK IF ALGO NAME EXISTS (should be last so i don't have to send queries)
    algo_with_append = f"{user}-{algo_name}"
    if modules.GET_SEARCH_ALGO_BY_NAME(algo_with_append) != "":
        return "False"
        
    return "True"

def CHECK_ACCOUNT_STATUS(User_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT User_id, User_Strikes, User_mute_status, User_timeout_status, User_ban_status
            
            FROM USERS
            
            WHERE User_id = '{User_id}'
        """)
        results = []
        for i in cursor.fetchall():
            results.append([
                i[0], # User_id
                i[1], # User_Strikes
                i[2], # User_mute_status
                i[3], # User_timeout_status
                i[4]  # User_ban_status
                ]
            )
            
        print("results", results)
            
        modules.close_conn(cursor, conn)         
        if results != []:
            if results[0][1] >= 10:
                return False
            # ELIF THE REST OF THE CHECKS FOR BAD BEHAVIOUR
            else: 
                return True
        else:
            return True
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

def CHECK_CHAT_ROOM_NAME(query_text):
    # 0. SPECIAL CHARACTERS  
    if any(not c.isalnum() for c in query_text):
    #    print(1)
        return "False" 
     
    # 1. CHECK LENGTH
    if len(query_text) > 20:
        # print(2)
        return "False"    
       
    # 2.  INJECTION CHECK
    if not modules.CHECK_INJECTION(query_text):
        # print(3)
        return "False"  
    
    return "True"

def CHECK_USER_ID_ROOM_CREATOR(user_id, room_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT COUNT(*)
            FROM CHAT_ROOMS
            WHERE Creator_id = '{user_id}'   
            AND Room_id = '{room_id}' 
        """)
        results = 0 
        for i in cursor.fetchall():
            results = i[0]
        modules.close_conn(cursor, conn)

        if str(results) != "0" or results != 0: # doublt JUST INCASE 
            return True
        else: 
            return False
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
  
def encrypt_caesar(plaintext,n=1):
    ans = ""
    # iterate over the given text
    for i in range(len(plaintext)):
        ch = plaintext[i]
        
        # check if space is there then simply add space
        if ch==" ":
            ans+=" "
        # check if a character is uppercase then encrypt it accordingly 
        elif (ch.isupper()):
            ans += chr((ord(ch) + n-65) % 26 + 65)
        # check if a character is lowercase then encrypt it accordingly
        
        else:
            ans += chr((ord(ch) + n-97) % 26 + 97)
    
    return ans  
    
def decrypt_caesar(encrypted_message, k=1):
        
    letters="abcdefghijklmnopqrstuvwxyz"

    decrypted_message = ""

    for ch in encrypted_message:

        if ch in letters:
            position = letters.find(ch)
            new_pos = (position - k) % 26
            new_char = letters[new_pos]
            decrypted_message += new_char
        else:
            decrypted_message += ch

    return decrypted_message

if __name__ == "__main__":
    pass



