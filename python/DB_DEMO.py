import inspect
try:
    from python.MODULES import *
except:
    from MODULES import *


def INSERT_DEMO_USER():
    print_title(f"{inspect.stack()[0][3]}")
    DB_INSERT.INSERT_USER("Andre", "password", "foreandr@gmail.com")
    DB_INSERT.INSERT_USER("Foreman", "password", "andrfore@gmail.com")

def INSERT_DEMO_CATEGORIES():
    print_title(f"{inspect.stack()[0][3]}")
    DB_INSERT.INSERT_CATEGORY("Noam Chomsky")

def INSERT_DEMO_POST():
    print_title(f"{inspect.stack()[0][3]}")
    DB_INSERT.INSERT_POST(Post_title="Noam Chomsky X TALK", Post_description="here is noam chomsky philosopher talking about x", Post_link="https://www.youtube.com/watch?v=J_jzFt8VLnk", User_id=1, Category="Noam Chomsky")

def INSERT_DEMO_TAGS():
    print_title(f"{inspect.stack()[0][3]}")
    DB_INSERT.INSERT_TAGS(Tag_name="philosophy", Tag_type="HARD", Post_id=1)
    DB_INSERT.INSERT_TAGS(Tag_name="philosophy", Tag_type="SOFT", Post_id=1)

def INSERT_DEMO_LIKES():
    print_title(f"{inspect.stack()[0][3]}")
    DB_INSERT.INSERT_LIKE(Post_id=1, User_id=1)
    
def INSERT_DEMO_DISLIKES():
    print_title(f"{inspect.stack()[0][3]}")
    DB_INSERT.INSERT_DISLIKE(Post_id=1, User_id=1)

def INSERT_DEMO_FAVOURITES():
    print_title(f"{inspect.stack()[0][3]}")
    DB_INSERT.INSERT_FAVOURITES(Post_id=1, User_id=1)

def INSERT_DEMO_COMMENTS():
    print_title(f"{inspect.stack()[0][3]}")
    DB_INSERT.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="baby girl")
    DB_INSERT.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello world", Replying_to_id=1)
    
def INSERT_DEMO_VIEWS():
    print_title(f"{inspect.stack()[0][3]}")
    DB_INSERT.INSERT_VIEWS(Post_id=1, User_id=1)
    DB_INSERT.INSERT_VIEWS(Post_id=1, User_id=1)

def INSERT_DEMO_CONNECTIONS():
    print_title(f"{inspect.stack()[0][3]}")
    DB_INSERT.INSERT_CONNECTION(user_id1=1, user_id2=2)
    DB_INSERT.INSERT_CONNECTION(user_id1=2, user_id2=1)

def INSERT_DEMO_IP_ADRESSES():
    print_title(f"{inspect.stack()[0][3]}")
    DB_INSERT.INSERT_IP_ADRESSES(Address="0.0.0.0", User_id=1)
    DB_INSERT.INSERT_IP_ADRESSES(Address="localhost", User_id=1)
    
def INSERT_DEMO_CHAT_ROOMS():
    print_title(f"{inspect.stack()[0][3]}")
    DB_INSERT.INSERT_CHAT_ROOMS(Creator_id=1, Room_name="hello world")
    DB_INSERT.INSERT_CHAT_ROOMS(Creator_id=1, Room_name="hello world2")
    DB_INSERT.INSERT_CHAT_ROOMS(Creator_id=2, Room_name="hello world3")
    
def INSERT_DEMO_CHAT_ROOMS_USER():
    print_title(f"{inspect.stack()[0][3]}")
    DB_INSERT.INSERT_CHAT_ROOMS_USER(User_id=1, Room_id=1)

def INSERT_DEMO_CHAT_ROOMS_ADMIN():
    print_title(f"{inspect.stack()[0][3]}")
    DB_INSERT.INSERT_CHAT_ROOMS_ADMIN(User_id=1, Room_id=1)

    
    
def FULL_DEMO_INSERT():
    INSERT_DEMO_USER()
    INSERT_DEMO_CATEGORIES()
    INSERT_DEMO_POST()
    INSERT_DEMO_TAGS()
    INSERT_DEMO_LIKES()
    INSERT_DEMO_DISLIKES()
    INSERT_DEMO_FAVOURITES()
    INSERT_DEMO_COMMENTS()
    INSERT_DEMO_VIEWS()
    INSERT_DEMO_CONNECTIONS()
    INSERT_DEMO_IP_ADRESSES()
    INSERT_DEMO_CHAT_ROOMS()
    INSERT_DEMO_CHAT_ROOMS_USER()
    INSERT_DEMO_CHAT_ROOMS_ADMIN()
    
if __name__ == "__main__": 
    DB_RESET.CREATE_TABLES()
    FULL_DEMO_INSERT()
