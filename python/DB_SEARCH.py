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
    
    
def GET_POST_LIKE_COUNT(home_function=False):
    if home_function:
        search_addition = "DESC,"
    else:
        search_addition = ""
    return f"""(SELECT COUNT(*) FROM LIKES likes WHERE likes.Post_id = posts.Post_id ){search_addition}""" 
        
def GET_POST_VIEW_COUNT(home_function=False):
    if home_function:
        search_addition = "DESC,"
    else:
        search_addition = ""    
    return f"""(SELECT COUNT(*) FROM VIEWS views WHERE views.Post_id = posts.Post_id){search_addition}"""
        
def GET_POST_COMMENT_COUNT(home_function=False):
    if home_function:
        search_addition = "DESC,"
    else:
        search_addition = ""
    return f"""( SELECT COUNT(*) FROM COMMENTS comments WHERE comments.Post_id = posts.Post_id){search_addition}"""
        
def GET_POST_FAVOURITE_COUNT(home_function=False):
    if home_function:
        search_addition = "DESC,"
    else:
        search_addition = ""
    return f"""(SELECT COUNT(*) FROM FAVOURITES favourites WHERE favourites.Post_id = posts.Post_id ){search_addition}"""
         
def GET_ALL_COUNTS():
    query = f"""
    {GET_POST_LIKE_COUNT(home_function=True)}
    {GET_POST_COMMENT_COUNT(home_function=True)}
    {GET_POST_FAVOURITE_COUNT(home_function=True)}
    {GET_POST_VIEW_COUNT(home_function=True)}
    """
    return query

def ORDER_CLAUSE_SECTIONS(clause):
    if clause.lower() == "Date".lower():
        return "posts.Date_Time,"
    
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

def TRANSFER_SEARCH_ORDER_CLAUSE_TO_QUERY(array_of_order_clauses):
    full_order_by = """"""
    try:
        for i in range(len(array_of_order_clauses)):
            print(i, array_of_order_clauses[i])
            full_order_by += ORDER_CLAUSE_SECTIONS(array_of_order_clauses[i])
    except Exception as e:
        print(str(e), str(array_of_order_clauses[i]), i)

    
    
    # end with this just becasue it's easier than finagling
    full_order_by += ("posts.Post_title")  
     
    # print(full_order_by)
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

    return f"(posts.Date_Time > current_date - interval '{date_needed}' day)" 

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
    properties = ["Likes", "Views", "Favourites"]
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
    
if __name__ == "__main__": 
    pass
