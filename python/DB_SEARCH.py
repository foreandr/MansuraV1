try:    
    import python.MODULES as modules
except:
    import MODULES as modules

def PERSON_SEARCH(person_id):
    if person_id == "" or str(person_id) == '0':
        # print("empty person id")
        return ""
    else:
        return F"AND post_person.Person_id = '{person_id}'"
    
def CHECK_PEOPLE_LETTER(letter):
    if letter != "":
        return F"AND LOWER(people.Person_name) LIKE LOWER('{letter}%')"
    return ""

def CHECK_PEOPLE_ORDER(sort_method):
    if sort_method == "alpha":
        return "ORDER BY Person_name ASC"
    elif sort_method == "beta": #demo
        return "ORDER BY DESC"
    else: return ""
    
def GET_POST_LIKE_COUNT():
    return """
    (   
        SELECT COUNT(*) 
        FROM LIKES likes
        WHERE likes.Post_id = posts.Post_id
    ),""" 
    
def GET_POST_VIEW_COUNT():
    return """(   
        SELECT COUNT(*) 
        FROM VIEWS views
        WHERE views.Post_id = posts.Post_id
    ), 
    """

def GET_POST_COMMENT_COUNT():
    return """
    (   
        SELECT COUNT(*) 
        FROM COMMENTS comments
        WHERE comments.Post_id = posts.Post_id
    ),
    """

def GET_POST_FAVOURITE_COUNT():
    return """(   
        SELECT COUNT(*) 
        FROM FAVOURITES favourites
        WHERE favourites.Post_id = posts.Post_id
    ),"""
    
def GET_ALL_COUNTS():
    query = f"""
    {GET_POST_LIKE_COUNT()}
    {GET_POST_COMMENT_COUNT()}
    {GET_POST_FAVOURITE_COUNT()}
    {GET_POST_VIEW_COUNT()}
    """
    return query
