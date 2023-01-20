from base64 import decode
import io
from PIL import Image
import inspect

try:    
    import python.MODULES as modules
except:
    import MODULES as modules


def CHECK_PERSON_IS_LIVE(person_id):
    try:
        cursor, conn = modules.create_connection()
        query = f"""
            SELECT Person_live
            FROM PEOPLE
            WHERE Person_id = '{person_id}'
        """
        cursor.execute(query)
        results = ""
        for i in cursor.fetchall():
            results = i[0]
            
        modules.close_conn(cursor, conn)
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_USERS_BY_TEXT(text):
    try:
        cursor, conn = modules.create_connection()
        query = f"""
            SELECT Person_name
            FROM PEOPLE
            WHERE LOWER(Person_name) LIKE LOWER('%{text}%')
            AND Person_live = 'True'
        """
        cursor.execute(query)
        results = []
        for i in cursor.fetchall():
            results.append(i[0])
            
        modules.close_conn(cursor, conn)
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_REAL_USERS_BY_TEXT(text, user_id):
    try:
        '''
        THE OR IN THIS FUNCTION CAN BE CHANGED TO REFLECT USER PRIVACY SETTINGS
        IF IT'S AND, THE FOLLOWING HAS TO BE MUTUAL TO CREATE A CHAT, ELSE ONE JUST HAS TO BE FOLLOWING THE OTHER
        '''
        # print("GET_USERS_BY_TEXT:", text)
        cursor, conn = modules.create_connection()
        query = f"""
            SELECT users.Username
            FROM USERS users
            WHERE LOWER(Username) LIKE LOWER('%{text}%')
            
            AND (
                    SELECT COUNT(*)
                    FROM CONNECTIONS
                    WHERE  
                    ( User_id1 = '{user_id}' AND users.User_id = User_id2 AND User_id2 = '{user_id}' OR users.User_id = User_id1)
                ) > 0   
        """
        cursor.execute(query)
        results = []
        for i in cursor.fetchall():
            results.append(i[0])
            
        modules.close_conn(cursor, conn)
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_USER_ID_FROM_NAME(username):
    print("username", username)
    try:
        cursor, conn = modules.create_connection()
        # print("NAME BEING USED", username)
        cursor.execute(f"""
            SELECT User_id 
            FROM USERS
            WHERE Username = %(username)s
        """, {'username': username}
        )
        
        for i in cursor.fetchall():
            modules.close_conn(cursor, conn)
            return i[0]
        return "NO ID"
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_USER_STRIKES_BY_ID(User_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT User_Strikes
            FROM USERS
            WHERE User_id = %(User_id)s
        """, {'User_id': User_id}
        )
        
        for i in cursor.fetchall():
            modules.close_conn(cursor, conn)
            return i[0]
        return 0
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_USER_NAME_FROM_ID(User_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT Username
            FROM USERS
            WHERE User_id = %(User_id)s
        """, {'User_id': User_id}
        )
        
        for i in cursor.fetchall():
            modules.close_conn(cursor, conn)
            return i[0]
        return "NO NAME"
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 
            
def GET_ALL_USERS():
    try:
        cursor, conn = modules.create_connection()
        query = """
            SELECT * FROM USERS
        """
        cursor.execute(query)
        
        for i in cursor.fetchall():
            print(i)
            
        modules.close_conn(cursor, conn)
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_POST_HTML_BY_ID(Post_id):
    try:
        cursor, conn = modules.create_connection()
        query = f"""
            SELECT Post_html 
            FROM POSTS
            WHERE Post_id = '{Post_id}'
        """
        cursor.execute(query)
        results = ""
        for i in cursor.fetchall():
            results = i[0]
            
        modules.close_conn(cursor, conn)
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_COUNT_COMMENTS_BY_ID(Post_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(F"""
            SELECT COUNT(*)
            FROM COMMENTS comments
            
            WHERE comments.Post_id = %(Post_id)s
        """, {'Post_id': Post_id})
        results = 0
        for i in cursor.fetchall():
            results = i[0]
            
        modules.close_conn(cursor, conn)
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def NEW_COMMENT_ORDER(new_comment):
    if new_comment == "true":
        new_comment_order = "ORDER BY comments.Date_time DESC"
    else:
        new_comment_order = ""
    return new_comment_order
    
def GET_NUM_COMMENT_VOTES_BY_ID(comment_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
        SELECT COUNT(*)
        FROM COMMENT_VOTES
        WHERE Comment_id = '{comment_id}'              
        """)
        
        results = 0
        for i in cursor.fetchall():
            results = i[0]
        modules.close_conn(cursor, conn)
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_N_COMMENTS(Post_id, N=3, comment_page_no=0, new_comment="false", check_order="likes"):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(F"""
            SELECT users.Username, comments.Comment_text, comments.Date_time, comments.Post_id, comments.Comment_id
            FROM COMMENTS comments
            
            INNER JOIN USERS users
            on users.User_id = comments.User_id
            
            WHERE comments.Post_id = %(Post_id)s
            
            {NEW_COMMENT_ORDER(new_comment)}
            
            OFFSET ( ({comment_page_no})  * {N} )
            LIMIT {N}
            """,{'Post_id': Post_id}
        )
        results = []
        
        for i in cursor.fetchall():
            results.append([i[0], i[1], i[2], i[3], i[4]])
        
        modules.close_conn(cursor, conn)
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 
    
def GET_ALL_POSTS():
    try:
        cursor, conn = modules.create_connection()
        query = """
            SELECT * FROM POSTS
        """
        cursor.execute(query)
        
        for i in cursor.fetchall():
            print(i)
            
        modules.close_conn(cursor, conn) 
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_ALL_COMMENTS():
    try:
        cursor, conn = modules.create_connection()
        query = """
            SELECT * FROM COMMENTS
        """
        cursor.execute(query)
        
        for i in cursor.fetchall():
            print(i)
            
        modules.close_conn(cursor, conn) 
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_ALL_TRIBUNAL_WORDS():
    try:
        cursor, conn = modules.create_connection()
        query = """
            SELECT Tribunal_word, 
            (   
                SELECT COUNT(*) 
                FROM TRIBUNAL_WORD_VOTE word_vote
                WHERE word_vote.Tribunal_word_id = word.Tribunal_word_id
                AND word_vote.Vote_type = 'UP'
            ),
            (   
                SELECT COUNT(*) 
                FROM TRIBUNAL_WORD_VOTE word_vote
                WHERE word_vote.Tribunal_word_id = word.Tribunal_word_id
                AND word_vote.Vote_type = 'DOWN'
            )
            
            FROM TRIBUNAL_WORD word
            ORDER BY Tribunal_word
            
        """
        cursor.execute(query)
        results = []
        for i in cursor.fetchall():
            results.append([i[0], i[1], i[2]])

        modules.close_conn(cursor, conn) 
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_WORD_PHRASE_ID_BY_NAME(phrase):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(F"""
        SELECT Tribunal_word_id
        FROM TRIBUNAL_WORD
        WHERE Tribunal_word = %(phrase)s  
        """, {'phrase': phrase}
        )
        results = 0
        for i in cursor.fetchall():
            results = i[0]
        modules.close_conn(cursor, conn) 
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_ALL_PEOPLE(sort_method, letter=""):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(F"""
            SELECT people.Person_id, 
            people.Person_name,        
            (   
                SELECT COUNT(*) 
                FROM POST_PERSON post_person
                WHERE post_person.Person_id = people.Person_id
            ) 
            
            FROM PEOPLE people
            WHERE 1=1
            {modules.CHECK_PEOPLE_LETTER(letter)}
            AND people.Person_live = 'True'
            {modules.CHECK_PEOPLE_ORDER(sort_method)}
        """)
        results = []
        for i in cursor.fetchall():
            results.append([i[0],i[1],i[2]])
            
        modules.close_conn(cursor, conn) 
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 
       
def GET_PROFILE_IMAGE_BY_USER(username):
    try:
        cursor, conn = modules.create_connection()
        query = f"""
            SELECT Profile_pic 
            FROM USERS
            WHERE username = %(username)s
        """, {'username': username}
        cursor.execute(query)
        byte_array = ""
        for i in cursor.fetchall():
            byte_array = bytes(i[0])
        
        #print(type(byte_array))
        #print(byte_array)
        # image = Image.open(io.BytesIO(byte_array))
        modules.close_conn(cursor, conn)
        return byte_array
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 
    
def GET_POST_ID_BY_LINK_AND_USER_ID(User_id, Post_link):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT Post_id
            FROM POSTS
            WHERE User_id = %(User_id)s
            AND Post_link = %(Post_link)s
            """, 
                {'User_id': User_id,
                'Post_link': Post_link
                }  
        )
        
        for i in cursor.fetchall():
            post_link = i[0]
        
        modules.close_conn(cursor, conn)
        return post_link
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_ROOM_ID_BY_TITLE_AND_USER_ID(User_id, Room_name):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT Room_id
            FROM CHAT_ROOMS
            WHERE Creator_id = %(User_id)s
            AND Room_name = %(Room_name)s
            """, 
                {'User_id': User_id,
                'Room_name': Room_name
                }  
        )
        Room_id = 1 
        for i in cursor.fetchall():
            Room_id = i[0]
        
        modules.close_conn(cursor, conn)
        return Room_id
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def CHECK_PERSON_EXISTS(Person):
    try:
        # print(F"{Person} is being checked for thier existence")
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
        SELECT COUNT(*)
        FROM PEOPLE
        WHERE LOWER(Person_name) = LOWER('{Person}')
        """)
        person_exists = 0
        for i in cursor.fetchall():
            person_exists = i[0]
        modules.close_conn(cursor, conn)
        if person_exists == 0:
            # print("does not exist")
            return False
        else:
            # print("does exist")
            return True
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 
  
def GET_PERSON_NAME_BY_ID(person_id):
    cursor, conn = modules.create_connection()
    cursor.execute(f"""
        SELECT Person_name
        FROM PEOPLE
        WHERE Person_id = '{person_id}'
    """)
        
    for i in cursor.fetchall():
        # print(i)
        person = i[0]
        
    modules.close_conn(cursor, conn)
    return person     

def GET_TAG_REQUESTS_BY_POST_ID(Post_id):
    cursor, conn = modules.create_connection()
    cursor.execute(f"""
        SELECT Post_id, Person_id, User_id
        FROM POST_PERSON_REQUEST
        WHERE Post_id = '{Post_id}'
    """)
    results = []
    for i in cursor.fetchall():
        results.append([
            i[0],
            i[1],
            i[2],
            modules.GET_PERSON_NAME_BY_ID(i[1]),
            modules.GET_USER_NAME_FROM_ID(i[2])
        ])
        
    modules.close_conn(cursor, conn)
    return results
    
def GET_NUM_PEOPLE_BY_POST_ID(Post_id):
    cursor, conn = modules.create_connection()
    cursor.execute(f"""
        SELECT COUNT(*)
        FROM POST_PERSON
        WHERE Post_id = '{Post_id}'         
    """)
    results = 0
    for i in cursor.fetchall():
        results = i[0]
    modules.close_conn(cursor, conn)
    return results

def GET_NUM_PEOPLE_REQUESTS_BY_POST_ID(Post_id):
    cursor, conn = modules.create_connection()
    cursor.execute(f"""
        SELECT COUNT(*)
        FROM POST_PERSON_REQUEST
        WHERE Post_id = '{Post_id}'         
    """)
    results = 0
    for i in cursor.fetchall():
        results = i[0]
    modules.close_conn(cursor, conn)
    return results
    

def GET_PERSON_ID_BY_NAME(Person, User_id):
    # CHECK IF PERSON EXISTS
    if not modules.CHECK_PERSON_EXISTS(Person):
        if User_id == 1: 
            modules.INSERT_PERSON(Person, Person_live="True")
        else:
            modules.INSERT_PERSON(Person, Person_live="False")
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT Person_id 
            FROM PEOPLE
            WHERE LOWER(Person_name) = LOWER(%(Person)s)
        """, {'Person': Person})
        
        for i in cursor.fetchall():
            # print(i)
            person = i[0]
        
        modules.close_conn(cursor, conn)
        return person
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_PERSON_ID_BY_POST_ID(Post_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT peeps.Person_id 
            FROM PEOPLE peeps
            
            INNER JOIN POST_PERSON post_person
            ON post_person.Person_id = peeps.Person_id
            
            WHERE post_person.Post_id = %(Post_id)s
        """, {'Post_id': Post_id})
        
        for i in cursor.fetchall():
            person = i[0]
        
        modules.close_conn(cursor, conn)
        return person
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 


def GET_POSTS_BY_PERSON(Person):
    return 1 

def GET_POSTS_BY_TAG(Person):
    return 1 

def GET_NUM_LIKES_BY_POST_ID(Post_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT COUNT(*) 
            FROM LIKES likes
            WHERE likes.Post_id = %(Post_id)s
        """, {'Post_id': Post_id}
        )
        results = 0
        for i in cursor.fetchall():
            results = i[0]
        modules.close_conn(cursor, conn)
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 
        
def GET_NUM_SUBSCRIBERS_BY_PERSON_ID(Person_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT COUNT(*) 
            FROM SUBSCRIPTIONS sub
            WHERE sub.Person_id = %(Person_id)s
        """, {'Person_id': Person_id}
        )
        results = 0
        for i in cursor.fetchall():
            results = i[0]
        modules.close_conn(cursor, conn)
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_NUM_FAVES_BY_POST_ID(Post_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT COUNT(*) 
            FROM FAVOURITES fave
            WHERE fave.Post_id = %(Post_id)s
        """, {'Post_id': Post_id}
        )
        results = 0
        for i in cursor.fetchall():
            results = i[0]
        modules.close_conn(cursor, conn)
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_NUM_SEARCH_FAVES_BY_SEARCH_ID(Search_algorithm_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT COUNT(*) 
            FROM SEARCH_ALGORITM_SAVE search_fave
            WHERE search_fave.Search_algorithm_id = %(Search_algorithm_id)s
        """, {'Search_algorithm_id': Search_algorithm_id}
        )
        results = 0
        for i in cursor.fetchall():
            results = i[0]
        modules.close_conn(cursor, conn)
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_NUM_VIEWS_BY_POST_ID(Post_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT COUNT(*) 
            FROM VIEWS views
            WHERE views.Post_id = %(Post_id)s
        """, {'Post_id': Post_id}
        )
        results = 0
        for i in cursor.fetchall():
            results = i[0]
        modules.close_conn(cursor, conn)
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 
        
def GET_NUM_COMMENTS_BY_POST_ID(Post_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT COUNT(*) 
            FROM COMMENTS comments
            WHERE comments.Post_id = %(Post_id)s
        """, {'Post_id': Post_id}
        )
        results = 0
        for i in cursor.fetchall():
            results = i[0]
        modules.close_conn(cursor, conn)
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_SEARCH_ALGO_BY_NAME(algo_name):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(F"""
        SELECT Search_algorithm_id, Search_algorithm_name
        FROM SEARCH_ALGORITHMS
        WHERE Search_algorithm_name = '{algo_name}'
        """
        )
        results = ""
        for i in cursor.fetchall():
            results = i[0]
            
        modules.close_conn(cursor, conn)
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_NUM_FAVOURITES_BY_POST_ID(Post_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT COUNT(*) 
            FROM FAVOURITES favs
            WHERE favs.Post_id = %(Post_id)s
        """, {'Post_id': Post_id}
        
        )
        results = 0
        for i in cursor.fetchall():
            results = i[0]
        modules.close_conn(cursor, conn)
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def SEARCH_DETAILS(searcher, person_id="", page_no=1):
    
    print("SEARCH DETAILS============")
    print("searcher      :", searcher)
    print("person_id     :", person_id)
    print("page_no       :", page_no)
    
    pass
def SEARCH_USER_HAS_LIKED(searcher_id):
    return f"""
        (
            SELECT COUNT(*)
            FROM LIKES likes
            WHERE likes.Post_id = posts.Post_id
            AND '{searcher_id}' = likes.User_id
        )
    """
def SEARCH_USER_HAS_SAVED(searcher_id):
    return f"""
        (
            SELECT COUNT(*)
            FROM FAVOURITES faves
            WHERE faves.Post_id = posts.Post_id
            AND '{searcher_id}' = faves.User_id
        )
    """     
def FAVOURITE_QUERY(favourites, searcher_id):
    if favourites:
        fave_string = F"AND faves.User_id = '{searcher_id}'"
        fave_inner_join = """
            INNER JOIN FAVOURITES faves
            ON faves.Post_id = posts.Post_id
        """
        return fave_string, fave_inner_join
    else:
        return "", ""
 
   
def SEARCH_QUERY(search_phrase):
    if search_phrase == "":
        return ""
    else:
        return F"""
    AND (
        LOWER(people.Person_name) LIKE LOWER('%{search_phrase}%') 
        OR LOWER(posts.Post_description) LIKE LOWER('%{search_phrase}%')
        OR LOWER(posts.Post_title) LIKE LOWER('%{search_phrase}%') 
    )"""

def GET_ORDER_CLAUSE_BY_SEARCH_ALGO_ID(search_algo_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT Search_order_clause
            FROM SEARCH_ALGORITHMS
            
            WHERE Search_algorithm_id = '{search_algo_id}'
        """)
            
        results = 1
        for i in cursor.fetchall():
            # print("search algo was not empty, returning:", i[0])
            results = i[0]
            
        modules.close_conn(cursor, conn)
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_WHERE_CLAUSE_BY_SEARCH_ALGO_ID(search_algo_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT Search_where_clause
            FROM SEARCH_ALGORITHMS
            WHERE Search_algorithm_id = '{search_algo_id}'
        """)
            
        results = 1
        for i in cursor.fetchall():
            # print("search algo was not empty, returning:", i[0])
            results = i[0]
            
        modules.close_conn(cursor, conn)
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def CHECK_IF_SUBSCRIBED(Person_id, User_id):

    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            (
                SELECT COUNT(*)
                FROM SUBSCRIPTIONS
                WHERE Person_id = '{Person_id}'
                AND User_id  = '{User_id}'
            )
            """)
            
        results = 0
        for i in cursor.fetchall():
            # print("search algo was not empty, returning:", i[0])
            results = i[0]
            
            
        modules.close_conn(cursor, conn)
        if str(results) != "0":
            return "True"
        else:
            return "False"
            
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 



def GET_MAX_POSTS(person_id):
    try:
        #THIS COULD SERIOUSLY SLOW THINGS DOWN
        cursor, conn = modules.create_connection()
        # count = 10000000 # arbitrary big number
        if person_id == '0' or person_id == "":
            person_query = ""
        else:
            person_query = f"""WHERE Person_id = '{person_id}'"""
        
        query = f"""
            SELECT COUNT(*)
            FROM POSTS posts
                
            INNER JOIN POST_PERSON post_per
            ON post_per.Post_id = POSTS.Post_id
            
            {person_query}   
        """
        cursor.execute(query)
            
        for i in cursor.fetchall():
            # print(i[0])
            count =  i[0]
        modules.close_conn(cursor, conn)
        return count 
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 
        
def GET_PEOPLE_BY_POST_ID(post_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT (
                SELECT Person_name
                FROM PEOPLE people
                
                WHERE post_person.Person_id =  people.Person_id
            )
            FROM POST_PERSON post_person
            WHERE post_id = '{post_id}'
        """)
        results = []
        for i in cursor.fetchall():
            results.append(i[0])
        
        modules.close_conn(cursor, conn)
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_PEOPLE_ID_BY_POST_ID(post_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT (
                SELECT Person_id
                FROM PEOPLE people
                
                WHERE post_person.Person_id =  people.Person_id
            )
            FROM POST_PERSON post_person
            WHERE post_id = '{post_id}'
        """)
        results = []
        for i in cursor.fetchall():
            results.append(i[0])
        
        modules.close_conn(cursor, conn)
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def CHECK_CAN_SCROLL(num_posts, max_posts):
    #print("NUM POSTS FOR QUERY :", num_posts)
    #print("MAX POSTS      :", max_posts)
    
    if num_posts > max_posts:
        # print("CANT SCROLL ANYMORE")
        return False
    else: 
        # print("SAFE TO SCROLL")
        return True
    
def GET_FOLLOWERS_BY_USER_ID(User_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT User_id1 
            FROM CONNECTIONS
            WHERE User_id2 = %(User_id)s
            """, {'User_id': User_id}
            )
        followers = []
        for i in cursor.fetchall():
            # print(i)
            followers.append(i[0])
            
        modules.close_conn(cursor, conn)
        return followers
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_FOLLOWING_BY_USER_ID(User_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT User_id2 
            FROM CONNECTIONS
            WHERE User_id1 = %(User_id)s
            """, {'User_id': User_id}
            )
        following = []
        for i in cursor.fetchall():
            # print(i)
            following.append(i[0])
            
        modules.close_conn(cursor, conn)
        return following
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def CHECK_IF_WORD_VOTE_EXISTS(word_id, user_id):
    try:
        cursor, _ = modules.create_connection()
        cursor.execute(f"""
            SELECT COUNT(*)
            FROM TRIBUNAL_WORD_VOTE
            WHERE User_id = %(word_id)s
            AND Tribunal_word_id = %(user_id)s
            """, {'word_id': word_id,
                'user_id': user_id
                }
        
        )
        count = 0
        for i in cursor.fetchall():
            count = i[0]
        
        if count > 0:
            return True
        else: return False
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_ALL_INTERACTIONS(User_id):
    try:
        cursor, conn = modules.create_connection()
        query = F"""
            SELECT users.User_id,
            (
                SELECT COUNT(*)
                FROM LIKES likes 
                WHERE likes.User_id = users.User_id
                AND Date_Time > now() - interval '30 second'
            ),
            (
                SELECT COUNT(*)
                FROM FAVOURITES faves
                WHERE faves.User_id = users.User_id
                AND Date_Time > now() - interval '30 second'
            ),
            (
                SELECT COUNT(*)
                FROM COMMENTS comments
                WHERE comments.User_id = users.User_id
                AND Date_Time > now() - interval '30 second'
            ),
            (
                SELECT COUNT(*)
                FROM COMMENT_VOTES comm_votes
                WHERE comm_votes.User_id = users.User_id
                AND Date_Time > now() - interval '30 second'
            ),
            (
                SELECT COUNT(*)
                FROM CONNECTIONS conn
                WHERE conn.User_id1 = users.User_id
                AND Date_Time > now() - interval '30 second'
            ),
            (
                SELECT COUNT(*)
                FROM  BLOCKS block
                WHERE block.User_id1 = users.User_id
                AND Date_Time > now() - interval '30 second'
            ),
            (
                SELECT COUNT(*)
                FROM  SEARCH_ALGORITHMS search
                WHERE search.User_id = users.User_id
                AND Date_Time > now() - interval '30 second'
            ),
            (
                SELECT COUNT(*)
                FROM  SEARCH_ALGORITM_VOTES search_votes
                WHERE search_votes.User_id = users.User_id
                AND Date_Time > now() - interval '30 second'
            ),
            (
                SELECT COUNT(*)
                FROM  SEARCH_ALGORITM_SAVE search_save
                WHERE search_save.User_id = users.User_id
                AND Date_Time > now() - interval '30 second'
            ),
            (
                SELECT COUNT(*)
                FROM  CHAT_ROOMS rooms
                WHERE rooms.Creator_id = users.User_id
                AND Date_Time > now() - interval '30 second'
            ),
            (
                SELECT COUNT(*)
                FROM  CHAT_MESSAGES messages
                WHERE messages.User_id = users.User_id
                AND Date_Time > now() - interval '30 second'
            )
            
            FROM USERS users
        
            WHERE users.User_id = '{User_id}'
        """
        results = []
        cursor.execute(query)
        for i in cursor.fetchall():
            # print(i)
            results.append([
                i[0], # USER_ID1
                i[1], # LIKES
                i[2], # FAVOURITES
                i[3], # COMMENTS
                i[4], # COMM VOTE
                i[5], # VIEW
                i[6], # CONN
                i[7],  # BLOCKS
                i[8], 
                i[9], 
                i[10], 
                i[11],  
                ])
            
        modules.close_conn(cursor, conn)
        results = results[0]
        # print(results)
        count = 0
        for i in range(1, len(results)):
            # print(results[i])
            count += results[i]
        if count > 30: # PROBABLY NEED TO REFINE THIS NUMBER
            modules.UPDATE_USER_STRIKES(User_id)
            
            # print("too much traffic from user")
            return False
        return True
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 
    
def GET_USER_CURRENT_SEARCH_ALGO_BY_ID(User_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT current.Search_algorithm_id,(
                SELECT Search_algorithm_name
                FROM SEARCH_ALGORITHMS search
                WHERE search.Search_algorithm_id = current.Search_algorithm_id
            )
            
            FROM CURRENT_USER_SEARCH_ALGORITHM current
            WHERE current.User_id = '{User_id}'
        """)
            
        results = [1, "Default"]
        for i in cursor.fetchall():
            # print("search algo was not empty, returning:", i[0])
            results = [i[0], i[1]]
            
        modules.close_conn(cursor, conn)
        return results[0], results[1]
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_SEARCH_ALGORITHM_DETAILS(user_id, search_type, limit_search="", page_no=1):
    try:
        cursor, conn = modules.create_connection()
        # print("limit search", limit_search)
        if search_type == "user":
            personal_or_global = f"AND ((search.User_id = '{user_id}') OR (SELECT COUNT(*) FROM SEARCH_ALGORITM_SAVE saved WHERE saved.Search_algorithm_id = search.Search_algorithm_id  AND  saved.User_id = '{user_id}') != 0)" 
        else:
            personal_or_global = ""
            
        if limit_search != "":
            constrain_algos = F"AND LOWER(search.Search_algorithm_name) LIKE LOWER('%{limit_search}%')"
        else:
            constrain_algos = ""
            
        posts_per_page = 100
        
        # print(" constrain_algos:",constrain_algos)    
        
        cursor.execute(f"""
            SELECT search.Search_algorithm_id, 
            search.Search_algorithm_name, 
            search.Search_where_clause, 
            search.Search_order_clause, 
            search.Date_time,
            (
                SELECT Username
                FROM Users users
                WHERE users.User_id = search.User_id
            ), 
            (
                SELECT COUNT(*)
                FROM SEARCH_ALGORITM_VOTES votes
                WHERE search.Search_algorithm_id = votes.Search_algorithm_id
            ),
            (
                SELECT COUNT(*)
                FROM SEARCH_ALGORITM_SAVE saved
                WHERE saved.Search_algorithm_id = search.Search_algorithm_id
                AND  saved.User_id = '{user_id}' 
            ),
            (
                SELECT COUNT(*)
                FROM SEARCH_ALGORITM_SAVE saved
                WHERE saved.Search_algorithm_id = search.Search_algorithm_id
            )
            
            FROM SEARCH_ALGORITHMS search
            
            WHERE 1=1
            {personal_or_global}
            {constrain_algos}

            ORDER BY (
                SELECT COUNT(*)
                FROM SEARCH_ALGORITM_VOTES votes
                WHERE search.Search_algorithm_id = votes.Search_algorithm_id
            ) DESC
            
            OFFSET ( ({page_no}-1)  * {posts_per_page} )
            LIMIT {posts_per_page};
        
        """)
        #break_counter = 0
        #break_number = 1000
        results = []
        for i in range((page_no-1) * posts_per_page):
            results.append([])
        
        for i in cursor.fetchall():
            #if break_number < break_counter:
            #    break 
            results.append([
                i[0], # search_id
                i[1], # name
                i[2], # where
                i[3], # order
                i[4], # date
                i[5], # GET_USER_NAME_FROM_ID(user_id),
                i[6], # count votes
                i[7], # has saved
                i[8]  # count saved
            ])
            # break_number =+1
            
        #for i in results:
        #    print(i)
        
        modules.close_conn(cursor, conn)
        return results, CAN_SCROLL_SEARCH(page_no, posts_per_page), page_no
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_TOTAL_MESSAGES_FOR_ROOM(room_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
        SELECT COUNT(*) 
        FROM CHAT_MESSAGES
        WHERE Room_id = '{room_id}'
        """)
        results = 0
        for i in cursor.fetchall():
            # print("TOTAL MESSAGES IN ROOM", i[0])
            results = i[0]
            
        modules.close_conn(cursor, conn)
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_TOTAL_POSTS_FOR_SEARCH():
    try:
        cursor, conn = modules.create_connection()
        cursor.execute("""
        SELECT COUNT(*) 
        FROM SEARCH_ALGORITHMS
        """)
        results = 0
        for i in cursor.fetchall():
            # print("TOTAL SEARCH ALGORITHMS", i[0])
            results = i[0]
            
        modules.close_conn(cursor, conn)
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 
            
def CAN_SCROLL_SEARCH(page_no, posts_per_page):
    total_posts_this_far = int(page_no) * posts_per_page
    if total_posts_this_far >= modules.GET_TOTAL_POSTS_FOR_SEARCH():
        return "False"
    else:
        return "True"

def GET_ALL_SEARCH_ALGOS():
    try:
        cursor, conn = modules.create_connection()
        cursor.execute("""
        SELECT Search_algorithm_name 
        FROM SEARCH_ALGORITHMS
        """)

        for i in cursor.fetchall():
            print(i)
            
        modules.close_conn(cursor, conn)
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 
    
def GET_SEARCH_FAVES():
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT *
            FROM SEARCH_ALGORITM_SAVE search_fave
            """
        )
        results = 0
        for i in cursor.fetchall():
            print(i)
        modules.close_conn(cursor, conn)
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_NUM_SEARCH_ALGOS_TODAY_BY_ID(User_id):
    if User_id == 1:
        return True
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
        SELECT COUNT(*)
        FROM SEARCH_ALGORITHMS
        WHERE Date_time BETWEEN NOW() - INTERVAL '24 HOURS' AND NOW()                 
        AND User_id = '{User_id}'
        """)
        results = 0
        for i in cursor.fetchall():
            results = i[0]
        modules.close_conn(cursor, conn)
        print(results)
        if results < 3:
            return True
        else:
            return False
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_NOTIFICATIONS(user_id, page_no):
    try:
        cursor, conn = modules.create_connection()
        posts_per_page = 10
        
        # GET ALL LIKES WHERE USER ID IS RECIPIENT
        cursor.execute(f"""
        SELECT likes.Like_id, likes.Date_time

        FROM LIKES likes
        
        INNER JOIN POSTS posts
        ON posts.User_id = likes.User_id
        
        INNER JOIN USERS users
        ON posts.User_id = users.User_id
        
        
        WHERE users.User_id = '{user_id}'
        
        OFFSET ( ({page_no}-1)  * {posts_per_page} )
        LIMIT {posts_per_page};               
        """)
        
        for i in cursor.fetchall():
            print(i)
        modules.close_conn(cursor, conn)
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 
    
def GET_CHAT_ROOM_DETAILS(User_id, page_no):
    try:
        cursor, conn = modules.create_connection()
        posts_per_page = 10
        cursor.execute(f"""
            SELECT Room_id, Room_name,
            (
                SELECT Username
                FROM USERS users
                WHERE rooms.Creator_id = users.User_id
            ),
            (
                SELECT COUNT(*)
                FROM CHAT_USERS chat_users
                -- WHERE rooms.Creator_id = chat_users.User_id
                WHERE rooms.Room_id = chat_users.Room_id
            )
            
            FROM CHAT_ROOMS rooms
            
            WHERE (
                SELECT COUNT(Room_id)
                FROM CHAT_USERS
                WHERE User_id = '{User_id}'
                AND rooms.Room_id = chat_users.Room_id
            ) > 0
            
            OFFSET ( ({page_no}-1)  * {posts_per_page} )
            LIMIT {posts_per_page};     
            
        """)
        results = []
        for i in cursor.fetchall():
            results.append([
                i[0],
                i[1],
                i[2],
                i[3]
            ])
        
        modules.close_conn(cursor, conn) 
        modules.print_green(F"{inspect.stack()[0][3]} COMPLETED")
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_CHAT_INVITE_DETAILS(User_id, page_no):
    try:
        posts_per_page = 10
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT invites.Room_id,
            (
                SELECT Room_name
                FROM CHAT_ROOMS rooms
                WHERE rooms.Room_id = invites.Room_id
            ),
            (
                SELECT Username
                FROM USERS users
                
                INNER JOIN CHAT_ROOMS rooms
                ON users.User_id = rooms.Creator_id
                
                WHERE rooms.Room_id = invites.Room_id
            ),
            (
                SELECT COUNT(*)
                FROM CHAT_USERS chat_users
                
                INNER JOIN CHAT_ROOMS rooms
                ON chat_users.User_id = rooms.Creator_id
                
                --WHERE rooms.Creator_id = chat_users.User_id
                WHERE rooms.Room_id = chat_users.Room_id
                AND rooms.Room_id = invites.Room_id
            )
            
            FROM CHAT_ROOM_INVITES invites 
            WHERE invites.User_id = '{User_id}'
            
            OFFSET ( ({page_no}-1)  * {posts_per_page} )
            LIMIT {posts_per_page};  
            
        """)

        results = []
        for i in cursor.fetchall():
            results.append([
                i[0],
                i[1],
                i[2],
                i[3]
            ])
        
        
        modules.close_conn(cursor, conn) 
        modules.print_green(F"{inspect.stack()[0][3]} COMPLETED")
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_CHAT_MESSAGES(room_id, page_no):
    try:
        cursor, conn = modules.create_connection()
        posts_per_page = 10
        cursor.execute(f"""
            SELECT 
            (
                SELECT Username
                FROM USERS users
                WHERE users.User_id = messages.User_id
            ), 
            messages.Date_time,
            messages.Message
            
            FROM CHAT_MESSAGES messages
            WHERE Room_id ='{room_id}'
            
            ORDER BY Date_time DESC
            
            OFFSET ( ({page_no}-1)  * {posts_per_page} )
            LIMIT {posts_per_page};        
        """)
        results = []
        for i in cursor.fetchall():
            results.append([
                i[0], #User_name, 
                i[1], #Date_time, 
                i[2], #Message
            ])
        
        modules.close_conn(cursor, conn) 
        modules.print_green(F"{inspect.stack()[0][3]} COMPLETED")
        return results, CAN_SCROLL_MESSAGES(page_no, posts_per_page, room_id)
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def CAN_SCROLL_MESSAGES(page_no, posts_per_page, room_id):
    total_posts_this_far = int(page_no) * posts_per_page
    if total_posts_this_far >= modules.GET_TOTAL_MESSAGES_FOR_ROOM(room_id):
        return "False"
    else:
        return "True"

def GET_ROOM_NAME_BY_ID(room_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT Room_name
            FROM CHAT_ROOMS
            WHERE Room_id = '{room_id}'
        """)
        results = ""
        for i in cursor.fetchall():
            results = i[0]
        modules.close_conn(cursor, conn) 
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

def GET_CREATOR_OF_ROOM(Room_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT Creator_id
            FROM CHAT_ROOMS
            WHERE Room_id = '{Room_id}'
        """)
        results = []
        for i in cursor.fetchall():
            results = i[0]

        modules.close_conn(cursor, conn) 
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

def GET_CHAT_ROOM_ID_BY_NAME(Room_name):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT Room_id
            FROM CHAT_ROOMS
            WHERE Room_name = '{Room_name}'
        """)
        results = []
        for i in cursor.fetchall():
            results = i[0]

        modules.close_conn(cursor, conn) 
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

def GET_CHAT_ROOM_NAMES_BY_TEXT(query_text, user_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT Room_name
            FROM CHAT_ROOMS rooms
            WHERE LOWER(Room_name) LIKE LOWER('%{query_text}%')
            AND (
                SELECT COUNT(Room_id)
                FROM CHAT_USERS chat_users
                WHERE User_id = '{user_id}'
                AND chat_users.Room_id = rooms.Room_id
            ) > 0
        """)
        results = []
        for i in cursor.fetchall():
            results.append(i[0])

        modules.close_conn(cursor, conn) 
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
def GET_ALL_USERS_IN_ROOM(Room_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT *
            FROM CHAT_USERS
            WHERE Room_id = '{Room_id}'
        """)
        # results = []
        for i in cursor.fetchall():
            print(i)

        modules.close_conn(cursor, conn) 
        # return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

def GET_CHAT_CREATOR_BY_ROOM(room_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT (
                SELECT Username
                FROM Users users
                WHERE users.User_id = rooms.Creator_id
            )
            FROM CHAT_ROOMS rooms
            WHERE rooms.Room_id = '{room_id}'
        """)
        results = []
        for i in cursor.fetchall():
            results = i[0]

        modules.close_conn(cursor, conn) 
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

def PERSON_LEADERBOARD_LIKES():
    return """
        (
            SELECT COUNT(*) 
            FROM LIKES likes
                    
            INNER JOIN POST_PERSON post_person
            ON post_person.Person_id = people.Person_id
                    
            INNER JOIN POSTS posts
            ON posts.Post_id = post_person.Post_id
                    
            WHERE likes.Post_id = posts.Post_id 
        )
    """
def PERSON_LEADERBOARD_COMMENTS():
    return """
        (
            SELECT COUNT(*) 
            FROM COMMENTS comments
                    
            INNER JOIN POST_PERSON post_person
            ON post_person.Person_id = people.Person_id
                    
            INNER JOIN POSTS posts
            ON posts.Post_id = post_person.Post_id
                    
            WHERE comments.Post_id = posts.Post_id 
        )
    """   
def PERSON_LEADERBOARD_VIEWS():
    return """
        (
            SELECT COUNT(*) 
            FROM VIEWS views
                    
            INNER JOIN POST_PERSON post_person
            ON post_person.Person_id = people.Person_id
                    
            INNER JOIN POSTS posts
            ON posts.Post_id = post_person.Post_id
                    
            WHERE views.Post_id = posts.Post_id 
        )
    """ 
def LEADERBOARD_PERSON(leaderboard_category):

    
    if leaderboard_category == 'likes':
        query_addition = modules.PERSON_LEADERBOARD_LIKES()
    elif leaderboard_category == "comments":
        query_addition = PERSON_LEADERBOARD_COMMENTS()
    elif leaderboard_category == "views":
        query_addition = PERSON_LEADERBOARD_VIEWS() 
        
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT Person_name,{query_addition},Person_id

            FROM PEOPLE people
            
            ORDER BY {query_addition}

            DESC
        """)
        results = []
        for i in cursor.fetchall():
            results.append([
                i[0], i[1], i[2]
            ])
        modules.close_conn(cursor, conn) 
        return results
    except Exception as e:    
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    

def USER_LEADERBOARD_LIKES():
    return """
    (
        SELECT COUNT(*) 
        FROM LIKES likes                        
        WHERE likes.User_id = users.User_id
    )
    """

def USER_LEADERBOARD_COMMENTS():
    return """
    (
        SELECT COUNT(*) 
        FROM COMMENTS comments                        
        WHERE comments.User_id = users.User_id
    )
    """

def USER_LEADERBOARD_VIEWS():
    return """
    (
        SELECT COUNT(*) 
        FROM VIEWS views                        
        WHERE views .User_id = users.User_id
    )
    """

def LEADERBOARD_USER(leaderboard_category):
    

    
    if leaderboard_category == 'likes':
        query_addition = modules.USER_LEADERBOARD_LIKES()
    elif leaderboard_category == "comments":
        query_addition = modules.USER_LEADERBOARD_COMMENTS()
    elif leaderboard_category == "views":
        query_addition = modules.USER_LEADERBOARD_VIEWS() 
    
    # print(query_addition)
    
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT Username, {query_addition}
            FROM Users users
            
            ORDER BY {query_addition}
            DESC
        """)
        results = []
        for i in cursor.fetchall():
            results.append([
                i[0], i[1]
            ])
        modules.close_conn(cursor, conn) 
        return results
    except Exception as e:    
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")    
           
def GET_ALL_PEOPLE_TESTING(letter):
    cursor, conn = modules.create_connection()
    cursor.execute(f"""
    SELECT Person_id, Person_name,
        (   
            SELECT COUNT(*) 
            FROM POST_PERSON post_person
            WHERE post_person.Person_id = people.Person_id
        ) 
    FROM People
    WHERE LOWER(people.Person_name) LIKE LOWER('{letter}%')
    ORDER BY Person_name DESC
    """)
    names = []
    for i in cursor.fetchall():
        names.append(i)
        # print(i)
    modules.close_conn(cursor, conn) 
    return names

def GET_USER_BY_NAME_LIKE(test):
    cursor, conn = modules.create_connection()
    cursor.execute(f"""
    SELECT Person_name
    FROM PEOPLE
    WHERE Lower(Person_name) = LOWER('{test}')
    """)
    names = []
    for i in cursor.fetchall():
        names.append(i[0])
        # print(i)

    
    modules.close_conn(cursor, conn) 
    return names
def GET_POST_DETAILS_BY_ID(Post_id):
    try:
        cursor, conn = modules.create_connection()
        query = f"""
            SELECT posts.Post_id, posts.Post_title
            FROM POSTS posts
            

            
            WHERE posts.Post_id = '{Post_id}'
        """
        cursor.execute(query)
        results = ""
        for i in cursor.fetchall():
            print(i)
            results = i[0]
            
        modules.close_conn(cursor, conn)
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def DEMO(User_id=1):
    following = GET_FOLLOWING_BY_USER_ID(1)
    print("following", following)
    cursor, conn = modules.create_connection()
    where_clause = '''
    AND (
    (
        SELECT COUNT(*) 
        FROM LIKES Likes        
        WHERE Likes.Post_id = posts.Post_id
    ) > 1
    
    )AND (
    (
        SELECT COUNT(*) 
        FROM COMMENTS Comments        
        WHERE Comments.Post_id = posts.Post_id
    ) > 1
    
    )AND (
    (
        SELECT COUNT(*) 
        FROM VIEWS Views        
        WHERE Views.Post_id = posts.Post_id
    ) > 1
    
    )AND (
    (
        SELECT COUNT(*) 
        FROM FAVOURITES Favourites        
        WHERE Favourites.Post_id = posts.Post_id
    ) > 0
    
    )
    '''
    cursor.execute(F"""
    SELECT Post_Id
    FROM POSTS posts
    
    
    WHERE 1=1
    {where_clause}
    
    LIMIT 600
    """)
    
    for i in cursor.fetchall():
        print(i)
        
    modules.close_conn(cursor, conn) 
    
    
def GET_NUM_POSTS():
    cursor, conn = modules.create_connection()
    cursor.execute("""SELECT COUNT(*) FROM POSTS""")
    
    for i in cursor.fetchall():
        print(i)
    modules.close_conn(cursor, conn) 

def CREATE_DEMO_ORDER_CLAUSE():
    return f"""
        (
            SELECT COUNT(*) 
            FROM LIKES likes 
                  
            INNER JOIN CONNECTIONS conn
            ON conn.User_id2 = likes.User_id
            
            WHERE likes.Post_id = posts.Post_id 
            AND conn.User_id1 = @SEARCHER_ID
        )DESC
    """ 

def GET_PEOPLE_DETAILS_BY_NAME(name):
    cursor, conn = modules.create_connection()
    cursor.execute(f"""
        SELECT *
        FROM PEOPLE
        WHERE Person_name LIKE '%{name}%'
        """)
    
    for i in cursor.fetchall():
        print(i)
    modules.close_conn(cursor, conn) 

def GET_TOP_N_PERSONS(amount):
    cursor, conn = modules.create_connection()
    cursor.execute(f"""
        SELECT PErson_name, Person_id
        FROM PEOPLE
        ORDER BY (
            (
            SELECT COUNT(*) 
            FROM LIKES likes
                    
            INNER JOIN POST_PERSON post_person
            ON post_person.Person_id = people.Person_id
                    
            INNER JOIN POSTS posts
            ON posts.Post_id = post_person.Post_id
                    
            WHERE likes.Post_id = posts.Post_id 
            ) + 
            (
            SELECT COUNT(*) 
            FROM VIEWS views
                    
            INNER JOIN POST_PERSON post_person
            ON post_person.Person_id = people.Person_id
                    
            INNER JOIN POSTS posts
            ON posts.Post_id = post_person.Post_id
                    
            WHERE views.Post_id = posts.Post_id 
            ) 
        )
        DESC
        LIMIT {amount}
        """)
    results = []
    for i in cursor.fetchall():
        results.append([i[0], i[1]])
    
    modules.close_conn(cursor, conn)     
    return results

def GET_TOP_N_USERS(amount):
    cursor, conn = modules.create_connection()
    cursor.execute(f"""
            SELECT Username, User_id
            FROM Users users
        ORDER BY (
            (
                SELECT COUNT(*) 
                FROM LIKES likes                        
                WHERE likes.User_id = users.User_id
            ) + 
            (
                SELECT COUNT(*) 
                FROM COMMENTS comments                        
                WHERE comments.User_id = users.User_id
            ) +
            (
            SELECT COUNT(*) 
            FROM VIEWS views                        
            WHERE views .User_id = users.User_id
            )
        )
        DESC
        LIMIT {amount}
        """)
    results = []
    for i in cursor.fetchall():
        results.append([i[0], i[1]])
    
    modules.close_conn(cursor, conn)     
    return results

if __name__ == "__main__":
    # modules.GET_PEOPLE_DETAILS_BY_NAME("w")
    print(modules.GET_USERS_BY_TEXT('w'))
    pass

