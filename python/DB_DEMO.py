import inspect
try:    
    import python.MODULES as modules
except:
    import MODULES as modules

def INSERT_DEMO_COMMENT_VOTE():
    modules.INSERT_COMMENT_VOTE(Comment_id=1, User_id=1, Vote_type="UP")
    modules.INSERT_COMMENT_VOTE(Comment_id=1, User_id=1, Vote_type="UP") 
    
    modules.INSERT_COMMENT_VOTE(Comment_id=2, User_id=1, Vote_type="UP")
    modules.INSERT_COMMENT_VOTE(Comment_id=1, User_id=3, Vote_type="UP")
    
    modules.INSERT_COMMENT_VOTE(Comment_id=1, User_id=1, Vote_type="UP")
    modules.INSERT_COMMENT_VOTE(Comment_id=2, User_id=2, Vote_type="UP")  

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
    modules.INSERT_PERSON("John Vervaeke")

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
    # modules.INSERT_POST(Post_title="SPOTIFY Peter Thiel X talk", Post_description="here is peter thiel philosopher talking about x", Post_link="https://open.spotify.com/episode/4CESb99rKgkQ5MvNL4HaFJ?si=3e1ea553d7c14637", User_id=1, Person="Peter Thiel") 
    modules.INSERT_POST(Post_title="tiktok Peter Thiel X talk", Post_description="here is peter thiel philosopher talking about x", Post_link="https://www.tiktok.com/@mazinosarchive/video/7177147474233150726?is_copy_url=1&is_from_webapp=v1", User_id=1, Person="Peter Thiel")
    # modules.INSERT_POST(Post_title="rumble Peter Thiel X talk", Post_description="here is peter thiel philosopher talking about x", Post_link="https://rumble.com/v10648s-paypal-co-founder-peter-thiel-bitcoin-keynote-bitcoin-2022-conference.html", User_id=1, Person="Peter Thiel")    
    # 
 
    # MICHAEL SUGRUE DEMO
    modules.INSERT_POST(Post_title="Michael Sugrue X talk", Post_description="here is michael sugrue philosopher talking about x", Post_link="https://www.youtube.com/watch?v=UlsR7_Wn8wc", User_id=1, Person="Michael Sugrue")
    modules.INSERT_POST(Post_title="Michael Sugrue X talk", Post_description="here is michael sugrue philosopher talking about x", Post_link="https://www.youtube.com/watch?v=_PSRVuQvVuU", User_id=1, Person="Michael Sugrue")
    modules.INSERT_POST(Post_title="Michael Sugrue X talk", Post_description="here is michael sugrue philosopher talking about x", Post_link="https://www.youtube.com/watch?v=WHiPfvzap3o", User_id=1, Person="Michael Sugrue")
    modules.INSERT_POST(Post_title="Michael Sugrue X talk", Post_description="here is michael sugrue philosopher talking about x", Post_link="https://www.youtube.com/watch?v=tyb93qZIC7g&t=1556s", User_id=1, Person="Michael Sugrue") 

    # VERVAEKE DEMO
    modules.INSERT_POST(Post_title="John Vervaeke X talk", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.youtube.com/watch?v=54l8_ewcOlY&t=1488s", User_id=1, Person="John Vervaeke") 
    modules.INSERT_POST(Post_title="John Vervaeke talk", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.youtube.com/watch?v=aF9HeXg65AE&t=71s", User_id=1, Person="John Vervaeke") 
    modules.INSERT_POST(Post_title="John Vervaeke X talk", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.youtube.com/watch?v=C1AaqD8t3pk", User_id=1, Person="John Vervaeke") 
    modules.INSERT_POST(Post_title="John Vervaeke X talk", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.youtube.com/watch?v=Lhl51bZQlM8", User_id=1, Person="John Vervaeke") 
    modules.INSERT_POST(Post_title="John Vervaeke X talk", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.youtube.com/watch?v=A_gH5VIZO0Q&t=158s", User_id=1, Person="John Vervaeke") 
    modules.INSERT_POST(Post_title="John Vervaeke X talk", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.youtube.com/watch?v=EWumJSBqXa8", User_id=1, Person="John Vervaeke") 
    modules.INSERT_POST(Post_title="John Vervaeke X talk", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.youtube.com/watch?v=39NpjQDtqNw", User_id=1, Person="John Vervaeke") 
    modules.INSERT_POST(Post_title="John Vervaeke X talk", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.youtube.com/watch?v=KoqibFwvQJ4", User_id=1, Person="John Vervaeke") 
    modules.INSERT_POST(Post_title="John Vervaeke X talk", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.youtube.com/watch?v=rpivf1SoEdc", User_id=1, Person="John Vervaeke") 
    modules.INSERT_POST(Post_title="John Vervaeke X talk", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.youtube.com/watch?v=hl2TE-mXPwM", User_id=1, Person="John Vervaeke") 
def INSERT_DEMO_SUBJECTS():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_SUBJECTS(Subject_name="philosophy", Subject_type="HARD", Post_id=1)
    modules.INSERT_SUBJECTS(Subject_name="philosophy", Subject_type="SOFT", Post_id=1)

def INSERT_DEMO_LIKES():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_LIKE(Post_id=1, User_id=1)
    
    modules.INSERT_LIKE(Post_id=1, User_id=2)
    modules.INSERT_LIKE(Post_id=2, User_id=2)
    modules.INSERT_LIKE(Post_id=3, User_id=2)
    modules.INSERT_LIKE(Post_id=4, User_id=2)
    
    modules.INSERT_LIKE(Post_id=1, User_id=3)
    modules.INSERT_LIKE(Post_id=2, User_id=3)
    modules.INSERT_LIKE(Post_id=3, User_id=3)
    modules.INSERT_LIKE(Post_id=4, User_id=3)
    
    
def INSERT_DEMO_DISLIKES():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_DISLIKE(Post_id=1, User_id=1)

def INSERT_DEMO_FAVOURITES():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_FAVOURITES(Post_id=1, User_id=1)

def INSERT_DEMO_COMMENTS():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="baby girl")
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello world i think noam chomsky is just the coolest guy ever hellow world testing testingn lololo hehe xd nono lol max tecxtkjsdahfalksjhdflakjhds", Replying_to_id=1)
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello world1", Replying_to_id=1)
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello world2", Replying_to_id=1)
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello world3")
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello world4", Replying_to_id=1)
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello world5")
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello world6", Replying_to_id=1)
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello world7", Replying_to_id=1)
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello world8", Replying_to_id=1)
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello world9", Replying_to_id=1)
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello world0")
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello world10", Replying_to_id=1)
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello world101")
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello world102", Replying_to_id=1)
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello world103", Replying_to_id=1)
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello world102334245", Replying_to_id=1)
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello world102345", Replying_to_id=2)
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello world10435", Replying_to_id=2)
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello world10564", Replying_to_id=2)
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello world1067")
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello world1087", Replying_to_id=2)
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello world10678", Replying_to_id=2)
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello world345103635")
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello wor3456ld10", Replying_to_id=2)
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello wo3456rld10", Replying_to_id=2)
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello w345orld10")
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello 63world10", Replying_to_id=2)
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello 445634565634563world10", Replying_to_id=3)
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello world10", Replying_to_id=3)
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello world")
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello w21456world10")
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello 456w3orld10", Replying_to_id=3)
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello 412world10", Replying_to_id=3)
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello 36345", Replying_to_id=4)
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello world10")
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello world10", Replying_to_id=4)
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello 12341234123world10", Replying_to_id=4)
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello 1234123412341234124world10")
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello w12341234123412341234orld10", Replying_to_id=3)
    modules.INSERT_COMMENTS(Post_id=1, User_id=1, Comment_text="hello wo123412341234rld10", Replying_to_id=3)
    
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
    INSERT_DEMO_COMMENT_VOTE()
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
