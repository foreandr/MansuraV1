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



        
def GET_COUNT_COMMENTS_BY_ID(Post_id):
    cursor, conn = modules.create_connection()
    query = F"""
        SELECT COUNT(*)
        FROM COMMENTS comments
        
        WHERE comments.Post_id = '{Post_id}'
    """
    cursor.execute(query)
    results = 0
    for i in cursor.fetchall():
        results = i[0]
        
    modules.close_conn(cursor, conn)
    return results


def GET_N_COMMENTS(Post_id, N=3, comment_page_no=0, new_comment="false", check_order="likes"):
    '''
    if new_comment == "true":
        new_comment_order = "ORDER BY comments.Date_time DESC"
    else:
        new_comment_order = ""
    '''
    if check_order == "alpha":
        comment_ordering = '''
            ORDER BY (SELECT COUNT(*) 
            FROM COMMENT_VOTES comm_vote_count
            WHERE comm_vote_count.Comment_id = comments.Comment_id
            AND word_vote.Vote_type = 'UP') 
        '''
    elif check_order == "likes":
        comment_ordering = '''
        
        '''
    
        
    cursor, conn = modules.create_connection()
    query = F"""
        SELECT users.Username, comments.Comment_text, comments.Date_time
        FROM COMMENTS comments
        
        INNER JOIN USERS users
        on users.User_id = comments.User_id
        
        WHERE comments.Post_id = '{Post_id}'
        
        
        OFFSET ( ({comment_page_no})  * {N} )
        LIMIT {N}
    """
    cursor.execute(query)
    results = []
    for i in cursor.fetchall():
        results.append([i[0], i[1], i[2]])
        
    modules.close_conn(cursor, conn)
    return results
    
def GET_ALL_POSTS():
    cursor, conn = modules.create_connection()
    query = """
        SELECT * FROM POSTS
    """
    cursor.execute(query)
    
    for i in cursor.fetchall():
        print(i)
        
    modules.close_conn(cursor, conn) 

def GET_ALL_COMMENTS():
    cursor, conn = modules.create_connection()
    query = """
        SELECT * FROM COMMENTS
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

def GET_NUM_LIKES_BY_POST_ID(Post_id):
    cursor, conn = modules.create_connection()
    cursor.execute(f"""
       
        SELECT COUNT(*) 
        FROM LIKES likes
        WHERE likes.Post_id = '{Post_id}'
    
    """)
    results = 0
    for i in cursor.fetchall():
        results = i[0]
    modules.close_conn(cursor, conn)
    return results

def GET_NUM_FAVES_BY_POST_ID(Post_id):
    cursor, conn = modules.create_connection()
    cursor.execute(f"""
       
        SELECT COUNT(*) 
        FROM FAVOURITES fave
        WHERE fave.Post_id = '{Post_id}'
    
    """)
    results = 0
    for i in cursor.fetchall():
        results = i[0]
    modules.close_conn(cursor, conn)
    return results

def GET_NUM_VIEWS_BY_POST_ID(Post_id):
    cursor, conn = modules.create_connection()
    cursor.execute(f"""
       
        SELECT COUNT(*) 
        FROM VIEWS views
        WHERE views.Post_id = '{Post_id}'
    
    """)
    results = 0
    for i in cursor.fetchall():
        results = i[0]
    modules.close_conn(cursor, conn)
    return results
    
def GET_NUM_COMMENTS_BY_POST_ID(Post_id):
    cursor, conn = modules.create_connection()
    cursor.execute(f"""
       
        SELECT COUNT(*) 
        FROM COMMENTS comments
        WHERE comments.Post_id = '{Post_id}'
    
    """)
    results = 0
    for i in cursor.fetchall():
        results = i[0]
    modules.close_conn(cursor, conn)
    return results

def GET_NUM_FAVOURITES_BY_POST_ID(Post_id):
    cursor, conn = modules.create_connection()
    cursor.execute(f"""
       
        SELECT COUNT(*) 
        FROM FAVOURITES favs
        WHERE favs.Post_id = '{Post_id}'
    
    """)
    results = 0
    for i in cursor.fetchall():
        results = i[0]
    modules.close_conn(cursor, conn)
    return results

def SEARCH_DETAILS(searcher, person_id="", page_no=1):
    print("SEARCH DETAILS============")
    print("searcher      :", searcher)
    print("person_id     :", person_id)
    print("page_no       :", page_no)

def SEARCH_USER_HAS_LIKED(searcher_id):
    return f"""
        (
            SELECT COUNT(*)
            FROM LIKES likes
            WHERE likes.Post_id = posts.Post_id
            AND '{searcher_id}' = likes.User_id
        ),
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

def UNIVERSAL_FUNCTION(searcher, person_id="", page_no=1):
    SEARCH_DETAILS(searcher=searcher, person_id=person_id, page_no=page_no)
    cursor, conn = modules.create_connection()
    person = modules.PERSON_SEARCH(person_id)
    searcher_id = GET_USER_ID_FROM_NAME(searcher) 
    posts_per_page = 9
    
    query = f"""
    SELECT 
    posts.Post_title, 
    posts.Post_description, 
    posts.Post_html, 
    posts.Date_time, 
    people.Person_name, 
    people.Person_id,
    posts.Post_id,
    {modules.GET_ALL_COUNTS()}
    {modules.SEARCH_USER_HAS_LIKED(searcher_id)}
    {modules.SEARCH_USER_HAS_SAVED(searcher_id)}
    
    
    FROM POSTS posts
    
    INNER JOIN POST_PERSON post_person
    ON post_person.Post_id = posts.Post_id
    
    INNER JOIN PEOPLE people
    ON people.Person_id = post_person.Person_id
    
    WHERE 1=1 
    {person}
    
    ORDER BY Person_name ASC
    
    OFFSET ( ({page_no}-1)  * {posts_per_page} )
    LIMIT {posts_per_page};
    """
    cursor.execute(query)
    posts = []
    for i in range((page_no-1) * posts_per_page):
        posts.append([])
    
    for i in cursor.fetchall():
        posts.append([
            i[0], #posts.Post_title, 
            i[1], #posts.Post_description, 
            i[2], #posts.Post_html, 
            i[3], #posts.Date_time, 
            i[4], #people.Person_name,
            i[5], #people.Person_id,
            i[6], # post_id#
            i[7], # count likes
            i[8], # count comments
            i[9], #count favourites 
            i[10], #count views 
            i[11], # has searcher liked post ( 0 == unliked)
            i[12], # has searcher SAVED post ( 0 == unliked)
        ])
        # print(i)
        
    modules.close_conn(cursor, conn)
    return query, posts, int(page_no), posts_per_page, CHECK_CAN_SCROLL(len(posts), GET_MAX_POSTS(person_id)), person_id


def GET_MAX_POSTS(person_id):
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
        print(i[0])
        count =  i[0]
    modules.close_conn(cursor, conn)
    return count 
        
def CHECK_CAN_SCROLL(num_posts, max_posts):
    print("NUM POSTS FOR QUERY :", num_posts)
    print("MAX POSTS      :", max_posts)
    
    if num_posts > max_posts:
        print("CANT SCROLL ANYMORE")
        return False
    else: 
        print("SAFE TO SCROLL")
        return True
    
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
    GET_ALL_COMMENTS()

