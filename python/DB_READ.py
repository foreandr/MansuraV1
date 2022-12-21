import io
from PIL import Image

try:    
    import python.MODULES as modules
except:
    import MODULES as modules


#

def GET_USER_ID_FROM_NAME(username):
    cursor, conn = modules.create_connection()
    query = f"""
        SELECT USer_id 
        FROM USERS
        WHERE Username = '{username}'
    """
    cursor.execute(query)
    
    for i in cursor.fetchall():
        modules.close_conn(cursor, conn)
        return i[0]
    return "NO NAME"
        
    
def GET_ALL_USERS():
    cursor, conn = modules.create_connection()
    query = """
        SELECT * FROM USERS
    """
    cursor.execute(query)
    
    for i in cursor.fetchall():
        print(i)
        
    modules.close_conn(cursor, conn)
    
def GET_ALL_POSTS():
    cursor, conn = modules.create_connection()
    query = """
        SELECT * FROM POSTS
    """
    cursor.execute(query)
    
    for i in cursor.fetchall():
        print(i)
        
    modules.close_conn(cursor, conn) 

def GET_ALL_TRIBUNAL_WORDS():
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


def GET_WORD_PHRASE_ID_BY_NAME(phrase):
    cursor, conn = modules.create_connection()
    cursor.execute(F"""
    SELECT Tribunal_word_id
    FROM TRIBUNAL_WORD
    WHERE Tribunal_word = '{phrase}'       
    """)
    results = 0
    for i in cursor.fetchall():
        results = i[0]
    modules.close_conn(cursor, conn) 
    return results




def GET_ALL_PEOPLE(sort_method, letter=""):
    cursor, conn = modules.create_connection()
    query = F"""
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
        {modules.CHECK_PEOPLE_ORDER(sort_method)}
        
        
    """
    cursor.execute(query)
    results = []
    for i in cursor.fetchall():
        results.append([i[0],i[1],i[2]])
        
    modules.close_conn(cursor, conn) 
    return results
     
    
def GET_PROFILE_IMAGE_BY_USER(username):
    cursor, conn = modules.create_connection()
    query = f"""
        SELECT Profile_pic 
        FROM USERS
        WHERE username = '{username}'
    """
    cursor.execute(query)
    byte_array = ""
    for i in cursor.fetchall():
        byte_array = bytes(i[0])
    
    #print(type(byte_array))
    #print(byte_array)
    # image = Image.open(io.BytesIO(byte_array))
    modules.close_conn(cursor, conn)
    return byte_array
    
    
def GET_POST_ID_BY_LINK_AND_USER_ID(User_id, Post_link):
    cursor, conn = modules.create_connection()
    query = f"""
        SELECT Post_id
        FROM POSTS
        WHERE User_id = '{User_id}'
        AND Post_link = '{Post_link}'
    """
    cursor.execute(query)
    
    for i in cursor.fetchall():
        post_link = i[0]
    
    modules.close_conn(cursor, conn)
    return post_link

def GET_PERSON_ID_BY_NAME(Person):
    cursor, conn = modules.create_connection()
    query = f"""
        SELECT Person_id 
        FROM PEOPLE
        WHERE Person_name = '{Person}'
    """
    cursor.execute(query)
    
    for i in cursor.fetchall():
        person = i[0]
    
    modules.close_conn(cursor, conn)
    return person

def GET_POSTS_BY_PERSON(Person):
    return 1 

def GET_POSTS_BY_TAG(Person):
    return 1 


def UNIVERSAL_FUNCTION(searcher, person_id=""):
    cursor, conn = modules.create_connection()
    person = modules.PERSON_SEARCH(person_id)
    searcher_id = GET_USER_ID_FROM_NAME(searcher) 

    
    query = f"""
    SELECT 
    posts.Post_title, 
    posts.Post_description, 
    posts.Post_html, 
    posts.Date_time, 
    people.Person_name, 
    people.Person_id,
    {modules.GET_ALL_COUNTS()}
    (
        SELECT COUNT(*)
        FROM LIKES likes
        WHERE likes.Post_id = posts.Post_id
        AND '{searcher_id}' = likes.User_id
    ),
 
    
    posts.Post_id
    FROM POSTS posts
    
    INNER JOIN POST_PERSON post_person
    ON post_person.Post_id = posts.Post_id
    
    INNER JOIN PEOPLE people
    ON people.Person_id = post_person.Person_id
    
    WHERE 1=1 
    {person}
    """
    cursor.execute(query)
    posts = []
    
    for i in cursor.fetchall():
        posts.append([
            i[0], #posts.Post_title, 
            i[1], #posts.Post_description, 
            i[2], #posts.Post_html, 
            i[3], #posts.Date_time, 
            i[4], #people.Person_name,
            i[5], #people.Person_id,
            i[6], #count likes
            i[7], #count comments
            i[8], #count favourites
            i[9], #count views
            i[10], # has searcher liked post
            
            
            # i[11], #BENCHMARK POST ID'S
        ])
        # print(i)
        
    modules.close_conn(cursor, conn)
    return posts

def GET_FOLLOWERS_BY_USER_ID(User_id):
    cursor, conn = modules.create_connection()
    query = f"""
        SELECT User_id1 
        FROM CONNECTIONS
        WHERE User_id2 = '{User_id}'
    """
    cursor.execute(query)
    followers = []
    for i in cursor.fetchall():
        # print(i)
        followers.append(i[0])
        
    modules.close_conn(cursor, conn)
    return followers

def CHECK_IF_WORD_VOTE_EXISTS(word_id, user_id):

    cursor, _ = modules.create_connection()
    cursor.execute(f"""
        SELECT COUNT(*)
        FROM TRIBUNAL_WORD_VOTE
        WHERE User_id = '{user_id}'
        AND Tribunal_word_id = '{word_id}'
    """)
    count = 0
    for i in cursor.fetchall():
        count = i[0]
    
    if count > 0:
        return True
    else: return False

if __name__ == "__main__": 

    GET_ALL_POSTS()
