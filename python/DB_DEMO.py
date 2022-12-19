import inspect
try:    
    import python.MODULES as modules
except:
    import MODULES as modules


def INSERT_DEMO_USER():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_USER("Andre", "password", "foreandr@gmail.com")
    modules.INSERT_USER("Foreman", "password", "andrfore@gmail.com")
    modules.INSERT_USER("David", "password", "david@gmail.com")

def INSERT_DEMO_CATEGORIES():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_CATEGORY("Noam Chomsky")

def INSERT_DEMO_POST():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_POST(Post_title="Noam Chomsky X TALK", Post_description="here is noam chomsky philosopher talking about x", Post_link="https://www.youtube.com/watch?v=J_jzFt8VLnk", User_id=1, Category="Noam Chomsky")

def INSERT_DEMO_TAGS():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_TAGS(Tag_name="philosophy", Tag_type="HARD", Post_id=1)
    modules.INSERT_TAGS(Tag_name="philosophy", Tag_type="SOFT", Post_id=1)

def INSERT_DEMO_LIKES():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_LIKE(Post_id=1, User_id=1)
    
def INSERT_DEMO_DISLIKES():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_DISLIKE(Post_id=1, User_id=1)

def INSERT_DEMO_FAVOURITES():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_FAVOURITES(Post_id=1, User_id=1)

def INSERT_DEMO_COMMENTS():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="baby girl")
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello world", Replying_to_id=1)
    
def INSERT_DEMO_VIEWS():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_VIEWS(Post_id=1, User_id=1)
    modules.INSERT_VIEWS(Post_id=1, User_id=1)

def INSERT_DEMO_CONNECTIONS():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_CONNECTION(user_id1=1, user_id2=2)
    modules.INSERT_CONNECTION(user_id1=2, user_id2=1)
    
def INSERT_DEMO_BLOCKS():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_BLOCKS(user_id1=3, user_id2=1)

def INSERT_DEMO_IP_ADRESSES():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_IP_ADRESSES(Address="0.0.0.0", User_id=1)
    modules.INSERT_IP_ADRESSES(Address="localhost", User_id=1)
    
def INSERT_DEMO_CHAT_ROOMS():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_CHAT_ROOMS(Creator_id=1, Room_name="hello world")
    modules.INSERT_CHAT_ROOMS(Creator_id=1, Room_name="hello world2")
    modules.INSERT_CHAT_ROOMS(Creator_id=2, Room_name="hello world3")
    
def INSERT_DEMO_CHAT_ROOMS_USER():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_CHAT_ROOMS_USER(User_id=1, Room_id=1)

def INSERT_DEMO_CHAT_ROOMS_ADMIN():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_CHAT_ROOMS_ADMIN(User_id=1, Room_id=1)

def INSERT_DEMO_REQUEST():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_REQUEST(User_id=1, Request_type="CATEGORY", Request_content="Steve Jobs")  
    
def FULL_DEMO_INSERT():
    INSERT_DEMO_USER()
    INSERT_DEMO_CATEGORIES()
    INSERT_DEMO_POST()
    INSERT_DEMO_TAGS()
    INSERT_DEMO_LIKES()
    # INSERT_DEMO_DISLIKES()
    INSERT_DEMO_FAVOURITES()
    INSERT_DEMO_COMMENTS()
    INSERT_DEMO_VIEWS()
    INSERT_DEMO_CONNECTIONS()
    INSERT_DEMO_BLOCKS()
    INSERT_DEMO_IP_ADRESSES()
    INSERT_DEMO_CHAT_ROOMS()
    INSERT_DEMO_CHAT_ROOMS_USER()
    INSERT_DEMO_CHAT_ROOMS_ADMIN()
    INSERT_DEMO_REQUEST()
    
if __name__ == "__main__": 
    modules.CREATE_TABLES()
    FULL_DEMO_INSERT()
