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

def INSERT_DEMO_PEOPLE():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_PERSON("Noam Chomsky")
    modules.INSERT_PERSON("Peter Thiel")
    modules.INSERT_PERSON("Michael Sugrue")

def INSERT_DEMO_POST():
    modules.print_title(f"{inspect.stack()[0][3]}")
    # CHOMSKY DEMO
    modules.INSERT_POST(Post_title="Noam Chomsky Ukraine 2 TALK", Post_description="here is noam chomsky philosopher talking about x", Post_link="https://www.youtube.com/watch?v=J_jzFt8VLnk", User_id=1, Person="Noam Chomsky")
    modules.INSERT_POST(Post_title="Noam Chomsky Ukraine 2 TALK", Post_description="here is noam chomsky philosopher talking about x", Post_link="https://www.youtube.com/watch?v=2IWkSTrfBdU", User_id=1, Person="Noam Chomsky")
    modules.INSERT_POST(Post_title="Noam Chomsky Ukraine 2 TALK", Post_description="here is noam chomsky philosopher talking about x", Post_link="https://www.youtube.com/watch?v=w_X5czMVKT8", User_id=1, Person="Noam Chomsky")
    modules.INSERT_POST(Post_title="Noam Chomsky Ukraine 2 TALK", Post_description="here is noam chomsky philosopher talking about x", Post_link="https://www.youtube.com/watch?v=XNSxj0TVeJs&t=1360s", User_id=1, Person="Noam Chomsky")
    modules.INSERT_POST(Post_title="Noam Chomsky Ukraine 2 TALK", Post_description="here is noam chomsky philosopher talking about x", Post_link="https://www.youtube.com/watch?v=aiJEmB3wBxM", User_id=1, Person="Noam Chomsky")
    
    # PETER THIEL DEMO
    modules.INSERT_POST(Post_title="Peter Thiel X talk", Post_description="here is peter thiel philosopher talking about x", Post_link="https://www.youtube.com/watch?v=XvKi7Omg1_M", User_id=1, Person="Peter Thiel")
    modules.INSERT_POST(Post_title="Peter Thiel X talk", Post_description="here is peter thiel philosopher talking about x", Post_link="https://www.youtube.com/watch?v=qYSnVR7d4VE", User_id=1, Person="Peter Thiel")
    modules.INSERT_POST(Post_title="Peter Thiel X talk", Post_description="here is peter thiel philosopher talking about x", Post_link="https://www.youtube.com/watch?v=F3EBfS9IcB4&t=2518s", User_id=1, Person="Peter Thiel")
    modules.INSERT_POST(Post_title="Peter Thiel X talk", Post_description="here is peter thiel philosopher talking about x", Post_link="https://www.youtube.com/watch?v=3Fx5Q8xGU8k&t=2553s", User_id=1, Person="Peter Thiel") 
    modules.INSERT_POST(Post_title="SPOTIFY Peter Thiel X talk", Post_description="here is peter thiel philosopher talking about x", Post_link="https://open.spotify.com/episode/4CESb99rKgkQ5MvNL4HaFJ?si=3e1ea553d7c14637", User_id=1, Person="Peter Thiel") 
    modules.INSERT_POST(Post_title="tiktok Peter Thiel X talk", Post_description="here is peter thiel philosopher talking about x", Post_link="https://www.tiktok.com/@mazinosarchive/video/7177147474233150726?is_copy_url=1&is_from_webapp=v1", User_id=1, Person="Peter Thiel")
    # modules.INSERT_POST(Post_title="rumble Peter Thiel X talk", Post_description="here is peter thiel philosopher talking about x", Post_link="https://rumble.com/v10648s-paypal-co-founder-peter-thiel-bitcoin-keynote-bitcoin-2022-conference.html", User_id=1, Person="Peter Thiel")    
    # 
 
    # MICHAEL SUGRUE DEMO
    modules.INSERT_POST(Post_title="Michael Sugrue X talk", Post_description="here is michael sugrue philosopher talking about x", Post_link="https://www.youtube.com/watch?v=UlsR7_Wn8wc", User_id=1, Person="Michael Sugrue")
    modules.INSERT_POST(Post_title="Michael Sugrue X talk", Post_description="here is michael sugrue philosopher talking about x", Post_link="https://www.youtube.com/watch?v=_PSRVuQvVuU", User_id=1, Person="Michael Sugrue")
    modules.INSERT_POST(Post_title="Michael Sugrue X talk", Post_description="here is michael sugrue philosopher talking about x", Post_link="https://www.youtube.com/watch?v=WHiPfvzap3o", User_id=1, Person="Michael Sugrue")
    modules.INSERT_POST(Post_title="Michael Sugrue X talk", Post_description="here is michael sugrue philosopher talking about x", Post_link="https://www.youtube.com/watch?v=tyb93qZIC7g&t=1556s", User_id=1, Person="Michael Sugrue") 




    
def INSERT_DEMO_SUBJECTS():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_SUBJECTS(Subject_name="philosophy", Subject_type="HARD", Post_id=1)
    modules.INSERT_SUBJECTS(Subject_name="philosophy", Subject_type="SOFT", Post_id=1)

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
    modules.INSERT_REQUEST(User_id=1, Request_type="PERSON", Request_content="Steve Jobs")  
    
def FULL_DEMO_INSERT():
    INSERT_DEMO_USER()
    INSERT_DEMO_PEOPLE()
    INSERT_DEMO_POST()
    INSERT_DEMO_SUBJECTS()
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

    answer = input("DO YOU WANT TO REALLY RESET?")
    if answer.lower() in ["y", "yes"]:
        modules.CREATE_TABLES("false")
        FULL_DEMO_INSERT()
