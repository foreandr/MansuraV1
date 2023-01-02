import io
from PIL import Image

try:    
    import python.MODULES as modules
except:
    import MODULES as modules


def GET_USERS_BY_TEXT(text):
    print("GET_USERS_BY_TEXT:", text)
    cursor, conn = modules.create_connection()
    query = f"""
        SELECT Person_name
        FROM PEOPLE
        WHERE LOWER(Person_name) LIKE LOWER('%{text}%')
    """
    cursor.execute(query)
    results = []
    for i in cursor.fetchall():
        results.append(i[0])
        
    modules.close_conn(cursor, conn)
    return results

def GET_USER_ID_FROM_NAME(username):
    cursor, conn = modules.create_connection()
    
    cursor.execute(f"""
        SELECT User_id 
        FROM USERS
        WHERE Username = %(username)s
    """, {'username': username}
    )
    
    for i in cursor.fetchall():
        modules.close_conn(cursor, conn)
        return i[0]
    return "NO NAME"

def GET_USER_NAME_FROM_ID(User_id):
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
            
def GET_ALL_USERS():
    cursor, conn = modules.create_connection()
    query = """
        SELECT * FROM USERS
    """
    cursor.execute(query)
    
    for i in cursor.fetchall():
        print(i)
        
    modules.close_conn(cursor, conn)

def GET_POST_HTML_BY_ID(Post_id):
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

def GET_COUNT_COMMENTS_BY_ID(Post_id):
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

def NEW_COMMENT_ORDER(new_comment):
    if new_comment == "true":
        new_comment_order = "ORDER BY comments.Date_time DESC"
    else:
        new_comment_order = ""
    return new_comment_order
    
def GET_N_COMMENTS(Post_id, N=3, comment_page_no=0, new_comment="false", check_order="likes"):

    cursor, conn = modules.create_connection()
    cursor.execute(F"""
        SELECT users.Username, comments.Comment_text, comments.Date_time
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
    WHERE Tribunal_word = %(phrase)s  
    """, {'phrase': phrase}
    )
    results = 0
    for i in cursor.fetchall():
        results = i[0]
    modules.close_conn(cursor, conn) 
    return results

def GET_ALL_PEOPLE(sort_method, letter=""):
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
        {modules.CHECK_PEOPLE_ORDER(sort_method)}
        
        
    """)
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
    
def GET_POST_ID_BY_LINK_AND_USER_ID(User_id, Post_link):
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

def GET_PERSON_ID_BY_NAME(Person):
    cursor, conn = modules.create_connection()
    cursor.execute(f"""
        SELECT Person_id 
        FROM PEOPLE
        WHERE Person_name = %(Person)s
    """, {'Person': Person})
    
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
        WHERE likes.Post_id = %(Post_id)s
    """, {'Post_id': Post_id}
    )
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
        WHERE fave.Post_id = %(Post_id)s
    """, {'Post_id': Post_id}
    )
    results = 0
    for i in cursor.fetchall():
        results = i[0]
    modules.close_conn(cursor, conn)
    return results

def GET_NUM_SEARCH_FAVES_BY_SEARCH_ID(Search_algorithm_id):
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

def GET_NUM_VIEWS_BY_POST_ID(Post_id):
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
    
def GET_NUM_COMMENTS_BY_POST_ID(Post_id):
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

def GET_SEARCH_ALGO_BY_NAME(algo_name):
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
    

def GET_NUM_FAVOURITES_BY_POST_ID(Post_id):
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

def IN_POST_TRIBUNAL(post_tribunal):
    if post_tribunal == False:
        return "AND posts.Post_live = 'True'"
    else:
        return "AND posts.Post_live != 'True'"
        
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
    cursor, conn = modules.create_connection()

    cursor.execute(f"""
        SELECT Search_order_clause
        FROM SEARCH_ALGORITHMS
        
        WHERE Search_algorithm_id = '{search_algo_id}'
    """)
        
    results = 1
    for i in cursor.fetchall():
        print("search algo was not empty, returning:", i[0])
        results = i[0]
        
    modules.close_conn(cursor, conn)
    return results

def GET_WHERE_CLAUSE_BY_SEARCH_ALGO_ID(search_algo_id):
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

  
def UNIVERSAL_FUNCTION(
        searcher, 
        searcher_id="", 
        person_id="",
        page_no=1, 
        favourites=False,
        post_tribunal=False,
        search_phrase="",
        ):
    '''
    print("searcher",searcher) 
    print("searcher_id",searcher_id) 
    print("person_id",person_id) 
    print("page_no",page_no)  
    print("favourites",favourites) 
    print("post_tribunal",post_tribunal) 
    print("search_phrase",search_phrase)
    ''' 
    
    cursor, conn = modules.create_connection()
    person = modules.PERSON_SEARCH(person_id)
    searcher_id = modules.GET_USER_ID_FROM_NAME(searcher) 
    fave_string, fave_inner_join = modules.FAVOURITE_QUERY(favourites, searcher_id)
    search_algo_id = modules.GET_USER_CURRENT_SEARCH_ALGO_BY_ID(searcher_id)
    
    # ORDER PARAMETERS
    order_clause = modules.GET_ORDER_CLAUSE_BY_SEARCH_ALGO_ID(search_algo_id)
    where_clause = modules.GET_WHERE_CLAUSE_BY_SEARCH_ALGO_ID(search_algo_id)
    
    posts_per_page = 3
    
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
    {modules.SEARCH_USER_HAS_LIKED(searcher_id)},
    {modules.SEARCH_USER_HAS_SAVED(searcher_id)},
    posts.Post_link 
    
    FROM POSTS posts
    
    INNER JOIN POST_PERSON post_person
    ON post_person.Post_id = posts.Post_id
    
    INNER JOIN PEOPLE people
    ON people.Person_id = post_person.Person_id
    
    {fave_inner_join}

    WHERE 1=1 
    {person}
    {fave_string}
    {IN_POST_TRIBUNAL(post_tribunal)}
    {SEARCH_QUERY(search_phrase)}
    {where_clause}
    
    ORDER BY {order_clause}
    
    OFFSET ( ({page_no}-1)  * {posts_per_page} )
    LIMIT {posts_per_page};
    """
    cursor.execute(query)
    posts = []
    for i in range((page_no-1) * posts_per_page):
        posts.append([])
    
    for i in cursor.fetchall():
        posts.append([
            i[0], # posts.Post_title, 
            i[1], # posts.Post_description, 
            i[2], # posts.Post_html, 
            i[3], # posts.Date_time, 
            i[4], # people.Person_name,
            i[5], # people.Person_id,
            i[6], # post_id#
            i[7], # count likes
            i[8], # count comments
            i[9], # count favourites 
            i[10], # count views 
            i[11], # has searcher liked post ( 0 == unliked)
            i[12], # has searcher SAVED post ( 0 == unliked)
            i[13], # post link
        ])
        # print(i)
        
    modules.close_conn(cursor, conn)
    return query, posts, int(page_no), posts_per_page, modules.CHECK_CAN_SCROLL(len(posts), modules.GETTING_POST_MAX_FROM_QUERY(query)), person_id

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
        # print(i[0])
        count =  i[0]
    modules.close_conn(cursor, conn)
    return count 
        
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

def CHECK_IF_WORD_VOTE_EXISTS(word_id, user_id):
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

def GET_ALL_INTERACTIONS(User_id):
    # print("RUNNING GET_ALL_INTERACTIONS")
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
            FROM VIEWS views
            WHERE views.User_id = users.User_id
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
            i[7]  # BLOCKS
            ])
        
    modules.close_conn(cursor, conn)
    results = results[0]
    # print(results)
    count = 0
    for i in range(1, len(results)):
        # print(results[i])
        count += results[i]
    if count > 20: # PROBABLY NEED TO REFINE THIS NUMBER
        # print("too much traffic from user")
        return False
    return True
    
def GET_USER_CURRENT_SEARCH_ALGO_BY_ID(User_id):
    cursor, conn = modules.create_connection()

    cursor.execute(f"""
        SELECT Search_algorithm_id
        FROM CURRENT_USER_SEARCH_ALGORITHM
        WHERE User_id = '{User_id}'
    """)
        
    results = 1
    for i in cursor.fetchall():
        # print("search algo was not empty, returning:", i[0])
        results = i[0]
        
    modules.close_conn(cursor, conn)
    return results

def GET_SEARCH_ALGORITHM_DETAILS(user_id, search_type):
    cursor, conn = modules.create_connection()
    
    if search_type == "user":
        personal_or_global = f"AND ((search.User_id = '{user_id}') OR (SELECT COUNT(*) FROM SEARCH_ALGORITM_SAVE saved WHERE saved.Search_algorithm_id = search.Search_algorithm_id  AND  saved.User_id = '{user_id}') != 0)" 
    else:
        personal_or_global = ""
        
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

        ORDER BY (
            SELECT COUNT(*)
            FROM SEARCH_ALGORITM_VOTES votes
            WHERE search.Search_algorithm_id = votes.Search_algorithm_id
        )
    
    """)
    break_counter = 0
    break_number = 1000
    results = []
    for i in cursor.fetchall():
        if break_number < break_counter:
            break 
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
        break_number =+1
    for i in results:
        print(i)
    modules.close_conn(cursor, conn)
    return results

def GET_ALL_SEARCH_ALGOS():
    cursor, conn = modules.create_connection()
    cursor.execute("""
    SELECT * 
    FROM SEARCH_ALGORITHMS
    """)

    for i in cursor.fetchall():
        print(i)
        
    modules.close_conn(cursor, conn)
    
def GET_SEARCH_FAVES():
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

if __name__ == "__main__": 

    GET_SEARCH_ALGORITHM_DETAILS(user_id=3, search_type="user")
    pass

