try:    
    import python.MODULES as modules
except:
    import MODULES as modules

import inspect
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
    
    
def GET_POST_LIKE_COUNT(
    home_function=False, 
    user_following_constraint=False,
    user_followers_constraint=False,
    user_constraint=False
    ):
    
    if home_function:
        search_addition = "DESC,"
    else:
        search_addition = ""
    
    # LIKED BY PEOPLE THE USER IS FOLLOWING
    if user_following_constraint:
        bias_user_likes_join = """INNER JOIN CONNECTIONS conn ON conn.User_id2 = likes.User_id"""
        bias_user_likes_and =  """AND conn.User_id1 = @SEARCHER_ID""" 
    else:
        bias_user_likes_join = ""
        bias_user_likes_and = ""
        
    
    # LIKES BY PEOPLE THE FOLLOWERS LIKED
    if user_followers_constraint:
        bias_followers_likes_join = """INNER JOIN CONNECTIONS conn2 ON conn2.User_id1 = likes.User_id"""
        bias_followers_likes_and =  """AND conn2.User_id2 = @SEARCHER_ID""" 
    else:
        bias_followers_likes_join = ""
        bias_followers_likes_and = ""
    
    # LIKES BY USER
    if user_constraint:
        user_constraint_str = "AND likes.User_id = @SEARCHER_ID"
    else:
        user_constraint_str = ""
    
    return f"""
    (
        SELECT COUNT(*) 
        FROM LIKES likes 
        {bias_user_likes_join}
        {bias_followers_likes_join}
        
        WHERE likes.Post_id = posts.Post_id
        {bias_user_likes_and}
        {user_constraint_str} 
        {bias_followers_likes_and}
    )
    {search_addition}""" 
    
def GET_POST_COMMENT_COUNT(    
    home_function=False, 
    user_following_constraint=False,
    user_followers_constraint=False,
    user_constraint=False):
    
    if home_function:
        search_addition = "DESC,"
    else:
        search_addition = ""
    
    # COMMENTS BY PEOPLE THE USER IS FOLLOWING
    if user_following_constraint:
        bias_user_comments_join = """INNER JOIN CONNECTIONS conn ON conn.User_id2 = comments.User_id"""
        bias_user_comments_and =  """AND conn.User_id1 = @SEARCHER_ID""" 
    else:
        bias_user_comments_join = ""
        bias_user_comments_and = ""
        
    # COMMENTS BY PEOPLE THE FOLLOWERS LIKED
    if user_followers_constraint:
        bias_followers_comments_join = """INNER JOIN CONNECTIONS conn2 ON conn2.User_id1 = comments.User_id"""
        bias_followers_comments_and =  """AND conn2.User_id2 = @SEARCHER_ID""" 
    else:
        bias_followers_comments_join = ""
        bias_followers_comments_and = ""
    
    # COMMENTS BY USER
    if user_constraint:
        user_constraint_str = "AND comments.User_id = @SEARCHER_ID"
    else:
        user_constraint_str = ""

    if home_function:
        search_addition = "DESC,"
    else:
        search_addition = ""
        
    return f"""
    (
        SELECT COUNT(*) 
        FROM COMMENTS comments 
        {bias_user_comments_join}
        {bias_followers_comments_join}
        
        WHERE comments.Post_id = posts.Post_id
        {bias_user_comments_and}
        {user_constraint_str} 
        {bias_followers_comments_and}
    )
    {search_addition}""" 

def GET_POST_VIEW_COUNT( 
    home_function=False, 
    user_following_constraint=False,
    user_followers_constraint=False,
    user_constraint=False):
    
    if home_function:
        search_addition = "DESC,"
    else:
        search_addition = ""
    
    # VIEWS BY PEOPLE THE USER IS FOLLOWING
    if user_following_constraint:
        bias_user_views_join = """INNER JOIN CONNECTIONS conn ON conn.User_id2 = views.User_id"""
        bias_user_views_and =  """AND conn.User_id1 = @SEARCHER_ID""" 
    else:
        bias_user_views_join = ""
        bias_user_views_and = ""
        
    # VIEWS BY PEOPLE THE FOLLOWERS LIKED
    if user_followers_constraint:
        bias_followers_views_join = """INNER JOIN CONNECTIONS conn2 ON conn2.User_id1 = views.User_id"""
        bias_followers_views_and =  """AND conn2.User_id2 = @SEARCHER_ID""" 
    else:
        bias_followers_views_join = ""
        bias_followers_views_and = ""
    
    # VIEWS BY USER
    if user_constraint:
        user_constraint_str = "AND views.User_id = @SEARCHER_ID"
    else:
        user_constraint_str = ""

    if home_function:
        search_addition = "DESC,"
    else:
        search_addition = ""
        
    return f"""
    (
        SELECT COUNT(*) 
        FROM VIEWS views
        {bias_user_views_join}
        {bias_followers_views_join}
        
        WHERE views.Post_id = posts.Post_id
        {bias_user_views_and}
        {user_constraint_str} 
        {bias_followers_views_and}
    )
    {search_addition}""" 
          
def GET_POST_FAVOURITE_COUNT(home_function=False, 
    user_following_constraint=False,
    user_followers_constraint=False,
    user_constraint=False):
    
    if home_function:
        search_addition = "DESC,"
    else:
        search_addition = ""
    
    # FAVOURITE BY PEOPLE THE USER IS FOLLOWING
    if user_following_constraint:
        bias_user_faves_join = """INNER JOIN CONNECTIONS conn ON conn.User_id2 = faves.User_id"""
        bias_user_faves_and =  """AND conn.User_id1 = @SEARCHER_ID""" 
    else:
        bias_user_faves_join = ""
        bias_user_faves_and = ""
        
    # FAVOURITE BY PEOPLE THE FOLLOWERS LIKED
    if user_followers_constraint:
        bias_followers_faves_join = """INNER JOIN CONNECTIONS conn2 ON conn2.User_id1 = faves.User_id"""
        bias_followers_faves_and =  """AND conn2.User_id2 = @SEARCHER_ID""" 
    else:
        bias_followers_faves_join = ""
        bias_followers_faves_and = ""
    
    # FAVOURITE BY USER
    if user_constraint:
        user_constraint_str = "AND faves.User_id = @SEARCHER_ID"
    else:
        user_constraint_str = ""

    if home_function:
        search_addition = "DESC,"
    else:
        search_addition = ""
        
    return f"""
    (
        SELECT COUNT(*) 
        FROM FAVOURITES faves
        {bias_user_faves_join}
        {bias_followers_faves_join}
        
        WHERE faves.Post_id = posts.Post_id
        {bias_user_faves_and}
        {user_constraint_str} 
        {bias_followers_faves_and}
    )
    {search_addition}""" 
         
def GET_POST_COMMENT_LIKE_COUNT(home_function=False, 
    user_following_constraint=False,
    user_followers_constraint=False,
    user_constraint=False):
    
    if home_function:
        search_addition = "DESC,"
    else:
        search_addition = ""
    
    # COMMENT LIKES BY PEOPLE THE USER IS FOLLOWING
    if user_following_constraint:
        bias_user_comment_likes_join = """INNER JOIN CONNECTIONS conn ON conn.User_id2 = comment_votes.User_id"""
        bias_user_comment_likes_and =  """AND conn.User_id1 = @SEARCHER_ID""" 
    else:
        bias_user_comment_likes_join = ""
        bias_user_comment_likes_and = ""
        
    
    # COMMENT LIKES BY PEOPLE THE FOLLOWERS LIKED
    if user_followers_constraint:
        bias_followers_comment_likes_join = """INNER JOIN CONNECTIONS conn2 ON conn2.User_id1 = comment_votes.User_id"""
        bias_followers_comment_likes_and =  """AND conn2.User_id2 = @SEARCHER_ID""" 
    else:
        bias_followers_comment_likes_join = ""
        bias_followers_comment_likes_and = ""
    
    # COMMENT LIKES BY USER
    if user_constraint:
        user_constraint_str = "AND comment_votes.User_id = @SEARCHER_ID"
    else:
        user_constraint_str = ""
    return f"""
        SELECT COUNT(*) 
        FROM COMMENT_VOTES comment_votes
        
        {bias_followers_comment_likes_join}
        {bias_user_comment_likes_join}
        
        INNER JOIN COMMENTS comments  
        ON comments.Comment_id = comment_votes.Comment_id        
        
        WHERE comments.Post_id = posts.Post_id
        {bias_user_comment_likes_and}
        {user_constraint_str} 
        {bias_followers_comment_likes_and}
    """        
         
def GET_ALL_COUNTS():
    query = f"""
    {GET_POST_LIKE_COUNT(home_function=True)}
    {GET_POST_COMMENT_COUNT(home_function=True)}
    {GET_POST_FAVOURITE_COUNT(home_function=True)}
    {GET_POST_VIEW_COUNT(home_function=True)}
    """
    return query

def ORDER_CLAUSE_SECTIONS(clause):
    if clause == "":
        pass
    
    # LIKES ORDER BY CLAUSES
    elif clause == "Order_Num_Likes_Total":
        return GET_POST_LIKE_COUNT()
    elif clause == "Order_Num_Likes_By_Me":
        return GET_POST_LIKE_COUNT(user_constraint=True)
    elif clause == "Order_Num_Likes_by_Followers":
        return GET_POST_LIKE_COUNT(user_followers_constraint=True)
    elif clause == "Order_Num_Likes_by_Following":
        return GET_POST_LIKE_COUNT(user_following_constraint=True)
    
    # COMMENTS ORDER BY CLAUSES
    elif clause == "Order_Num_Comments_Total":
        return GET_POST_COMMENT_COUNT()
    elif clause == "Order_Num_Comments_By_Me":
        return GET_POST_COMMENT_COUNT(user_constraint=True)
    elif clause == "Order_Num_Comments_by_Followers":
        return GET_POST_COMMENT_COUNT(user_followers_constraint=True)
    elif clause == "Order_Num_Comments_by_Following":
        return GET_POST_COMMENT_COUNT(user_following_constraint=True)
    
    # VIEWS ORDER BY CLAUSES
    elif clause == "Order_Num_Views_Total":
        return GET_POST_VIEW_COUNT()
    elif clause == "Order_Num_Views_By_Me":
        return GET_POST_COMMENT_COUNT(user_constraint=True)
    elif clause == "Order_Num_Views_by_Followers":
        return GET_POST_COMMENT_COUNT(user_followers_constraint=True)
    elif clause == "Order_Num_Views_by_Following":
        return GET_POST_COMMENT_COUNT(user_following_constraint=True)
    
    # FAVES ORDER BY CLAUSES
    elif clause == "Order_Num_Favourites_Total":
        return GET_POST_FAVOURITE_COUNT()
    elif clause == "Order_Num_Favourites_By_Me":
        return GET_POST_FAVOURITE_COUNT(user_constraint=True)
    elif clause == "Order_Num_Favourites_by_Followers":
        return GET_POST_FAVOURITE_COUNT(user_followers_constraint=True)
    elif clause == "Order_Num_Favourites_by_Following":
        return GET_POST_FAVOURITE_COUNT(user_following_constraint=True)
    
    # COMMENT LIKES COMMENT LIKES BY CLAUSES
    elif clause == "Order_Num_Comment_Likes_Total":
        return GET_POST_COMMENT_LIKE_COUNT()
    elif clause == "Order_Num_Comment_Likes_By_Me":
        return GET_POST_COMMENT_LIKE_COUNT(user_constraint=True)
    elif clause == "Order_Num_Comment_Likes_by_Followers":
        return GET_POST_COMMENT_LIKE_COUNT(user_followers_constraint=True)
    elif clause == "Order_Num_Comment_Likes_by_Following":
        return GET_POST_COMMENT_LIKE_COUNT(user_following_constraint=True)

def OLD_UNUSED_ORDER_CLAUSE_SECTIONS(clause):
    """THIS IS WHAT I WAS USING BEFORE MAKING THE SWITCH TO CHECKBOXES
    if clause.lower() == "Date".lower():
        return "posts.Date_Time DESC,"
    
    elif clause.lower() == "Likes".lower():
        return GET_POST_LIKE_COUNT(True)
    
    elif clause.lower() == "Favourites".lower():
        return GET_POST_FAVOURITE_COUNT(True)
    
    elif clause.lower() == "Comments".lower():
        return GET_POST_COMMENT_COUNT(True)
    
    elif clause.lower() == "Views".lower():
        return GET_POST_VIEW_COUNT(True)
    
    elif clause.lower() == "Alpha_Title".lower():
        return "posts.Post_title DESC,"
    
    elif clause.lower() == "Likes_Views".lower():
        return (F"({GET_POST_VIEW_COUNT()}+{GET_POST_LIKE_COUNT()}) DESC,")
    
    elif clause.lower() == "Likes_Favourites".lower():
        return (F"({GET_POST_FAVOURITE_COUNT()}+{GET_POST_LIKE_COUNT()}) DESC,")
    
    elif clause.lower() == "Likes_Favourites_Comments".lower():
        return (F"({GET_POST_FAVOURITE_COUNT()}+{GET_POST_LIKE_COUNT()}+{GET_POST_COMMENT_COUNT()}) DESC,")
    
    elif clause.lower() == "Likes_Favourites_Comments_Views".lower():
        return (F"({GET_POST_FAVOURITE_COUNT()}+{GET_POST_LIKE_COUNT()}+{GET_POST_COMMENT_COUNT()}+{GET_POST_VIEW_COUNT()}) DESC,")
    """
    
def GET_BIAS_TYPE_FROM_ARRAY(html_clause):
    if "Order_Num_Likes" in html_clause: 
        bias_type = "like_bias"
        
    elif "Order_Num_Views" in html_clause:
        bias_type = "views_bias"
        
    elif "Order_Num_Favourites" in html_clause:
        bias_type = "faves_bias"
        
    elif "Order_Num_Comments" in html_clause:
        bias_type = "comments_bias"
        
    elif "Order_Num_Comment_Likes" in html_clause:
        bias_type = "comment_likes_bias"
    
    return bias_type
    
def TRANSFER_SEARCH_ORDER_CLAUSE_TO_QUERY(array_of_order_clauses, bias_dict):
    full_order_by = """"""
    print("BIAS DICT", bias_dict)
    try:
        for i in range(len(array_of_order_clauses)):
            bias_type = GET_BIAS_TYPE_FROM_ARRAY(array_of_order_clauses[i])
            bias_number = bias_dict[bias_type]
            print(i, array_of_order_clauses[i], bias_type, bias_number)
            
            if i == len(array_of_order_clauses) - 1:
                full_order_by += f"(({ORDER_CLAUSE_SECTIONS(array_of_order_clauses[i])}) * {bias_number})"
            else:
                full_order_by += f"(({ORDER_CLAUSE_SECTIONS(array_of_order_clauses[i])}) * {bias_number})" + "+"
            
            
    except Exception as e:
        pass
        # print(str(e), str(array_of_order_clauses[i]), i)
        # TODO:log this

    # print(full_order_by)
    
    # end with this just becasue it's easier than finagling
    #todo:GOTTA ADD DESC TO THE END along with a plus sign to add queries
    print("QUERY BELOW:")
    # full_order_by += ("posts.Post_title")  
    print(full_order_by)
    exit()
    return full_order_by

def TRANSLATE_DATE_CLAUSES(date_clause):
    if date_clause == "All Time":
        return ""
    
    if date_clause.lower() == "Today".lower():
        date_needed = 1
    elif date_clause.lower() == "This Week".lower():
        date_needed = 7
    elif date_clause.lower() == "This Month".lower():
        date_needed = 30
    elif date_clause.lower() == "This Year".lower():
        date_needed = 365

    return f"(posts.Date_Time > current_date - interval ''{date_needed}'' day)" 

def TRANSLATE_CONDITIONAL(conditional):
    if conditional.lower() == "Greater Than".lower():
        return ">="
    else:
        return "<="
    
def TRANSLATE_PROPERTIES(properties):
    if properties.lower() == "Likes".lower():
        return GET_POST_LIKE_COUNT(False)
    elif properties.lower() == "Views".lower():
        return GET_POST_VIEW_COUNT(False)
    elif properties.lower() == "Favourites".lower():
        return GET_POST_FAVOURITE_COUNT(False)
    elif properties.lower() == "Comments".lower():
        return GET_POST_COMMENT_COUNT(False)
    
def WHERE_CLAUSE_SECTIONS(clause):
    # print(clause)
    if "All Time" in clause:
        return ""

    date_clauses = ["All Time","This Week","This Month","This Year", "Today"]
    conditional_clauses = ["AND", "OR"]
    properties = ["Likes", "Views", "Favourites", "Comments"]
    comparison = ["Less Than", "Equal", "Greater Than"]
    numbers = ["10", "100", "1000", "10000","100000", "1000000","10000000"]
    
    
    sectioned_clause = clause.split(",")
    full_where_clause = ""
    for i in range(len(sectioned_clause)):
        # print("sectioned_clause[i]", len(sectioned_clause[i]), sectioned_clause[i])
        value = ""
        if sectioned_clause[i] in date_clauses:
            value = TRANSLATE_DATE_CLAUSES(sectioned_clause[i])
        
        elif sectioned_clause[i] in conditional_clauses:
            value = sectioned_clause[i] + " " 
        
        elif sectioned_clause[i] in properties:
            # print("conditional_clauses", sectioned_clause[i])
            value = TRANSLATE_PROPERTIES(sectioned_clause[i])
    
        elif sectioned_clause[i] in comparison:
            # print("comparison", sectioned_clause[i])
            value = TRANSLATE_CONDITIONAL(sectioned_clause[i])
    
        elif sectioned_clause[i] in numbers:
            # print("numbers", sectioned_clause[i])
            value = sectioned_clause[i]
        
        full_where_clause += value
        # print(i, full_where_clause)

        
            
    # print("full_where_clause\n", full_where_clause)
    return full_where_clause


def TRANSFER_SEARCH_WHERE_TO_QUERY(array_of_where_clauses):
    full_where = """"""
    for i in array_of_where_clauses:
        full_where += WHERE_CLAUSE_SECTIONS(i) + "\n"
    # end with this just becasue it's easier than finagling
    return full_where
    
def UNIVERSAL_FUNCTION(
        searcher, 
        searcher_id="", 
        person_id="",
        page_no=1, 
        favourites=False,
        post_tribunal=False,
        profile_id="",
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
    try:
        cursor, conn = modules.create_connection()
        person = modules.PERSON_SEARCH(person_id)
        searcher_id = modules.GET_USER_ID_FROM_NAME(searcher) 
        fave_string, fave_inner_join = modules.FAVOURITE_QUERY(favourites, searcher_id)
        search_algo_id, _ = modules.GET_USER_CURRENT_SEARCH_ALGO_BY_ID(searcher_id)
        
        # SPECIFIC TO USER
        if profile_id != "":
            user_profile = f"AND posts.User_id = '{profile_id}'"
        else:
            user_profile = ""
            
        # print("user profile", user_profile)
        
        # ORDER PARAMETERS
        #order_clause = modules.GET_ORDER_CLAUSE_BY_SEARCH_ALGO_ID(search_algo_id)
        order_clause = modules.CREATE_DEMO_ORDER_CLAUSE()
        order_clause = order_clause.replace("@SEARCHER_ID", str(searcher_id))
        
        where_clause = modules.GET_WHERE_CLAUSE_BY_SEARCH_ALGO_ID(search_algo_id)
        
        # CAST VOTE FOR SEARCH
        modules.INSERT_SEARCH_VOTE(search_algo_id, searcher_id)
        
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
        posts.Post_link,
        (SELECT Username FROM USERS users WHERE posts.User_id = users.User_id),
        posts.User_id,
        people.Person_live
            
        FROM POSTS posts
        
        INNER JOIN POST_PERSON post_person
        ON post_person.Post_id = posts.Post_id
        
        INNER JOIN PEOPLE people
        ON people.Person_id = post_person.Person_id
        
        {fave_inner_join}

        WHERE 1=1 
        {person}
        {fave_string}
        {modules.IN_POST_TRIBUNAL(post_tribunal)}
        {modules.SEARCH_QUERY(search_phrase)}
        {where_clause}
        {user_profile}
        
        ORDER BY {order_clause}
        
        OFFSET ( ({page_no}-1)  * {posts_per_page} )
        LIMIT {posts_per_page};
        """
        
        #LOG THE QUERY [ERROR CHECKING]
        # modules.log_function(msg_type="test", log_string=query, function_name=f"{inspect.stack()[0][3]}")

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
                i[14], # UPLOADER name
                i[15], # UPLOADER id
                i[16], # person live
                modules.GET_PEOPLE_BY_POST_ID(i[6]),
                modules.GET_PEOPLE_ID_BY_POST_ID(i[6])
            ])
            # print(i)
            
        modules.close_conn(cursor, conn)
        return query, posts, int(page_no), posts_per_page, modules.CHECK_CAN_SCROLL(len(posts), modules.GETTING_POST_MAX_FROM_QUERY(query)), person_id
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 
if __name__ == "__main__": 
    pass
