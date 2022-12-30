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
    modules.INSERT_USER("Andre", "helloWorld!", "foreandr@gmail.com")
    modules.INSERT_USER("Foreman", "helloWorld!", "andrfore@gmail.com")
    modules.INSERT_USER("David", "helloWorld!", "david@gmail.com")

def INSERT_DEMO_ADMIN():
    modules.INSERT_POST_ADMIN(1)
    
    
def INSERT_DEMO_PEOPLE():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_PERSON("Noam Chomsky")
    modules.INSERT_PERSON("Peter Thiel")
    modules.INSERT_PERSON("Michael Sugrue")
    modules.INSERT_PERSON("John Vervaeke")

def INSERT_DEMO_POST():
    modules.print_title(f"{inspect.stack()[0][3]}")
    # CHOMSKY DEMO
    
    modules.INSERT_POST(Post_title="Noam Chomsky Ukraine 2 TALK2", Post_description="here is noam chomsky philosopher talking about x", Post_link="https://www.youtube.com/watch?v=J_jzFt8VLnk", Post_live="True", User_id=1, Person="Noam Chomsky")
    modules.INSERT_POST(Post_title="Noam Chomsky Ukraine 2 TALK3", Post_description="here is noam chomsky philosopher talking about x", Post_link="https://www.youtube.com/watch?v=2IWkSTrfBdU", Post_live="True", User_id=1, Person="Noam Chomsky")
    modules.INSERT_POST(Post_title="Noam Chomsky Ukraine 2 TALK4", Post_description="here is noam chomsky philosopher talking about x", Post_link="https://www.youtube.com/watch?v=w_X5czMVKT8", Post_live="True", User_id=1, Person="Noam Chomsky")
    modules.INSERT_POST(Post_title="Noam Chomsky Ukraine 2 TALK5", Post_description="here is noam chomsky philosopher talking about x", Post_link="https://www.youtube.com/watch?v=XNSxj0TVeJs&t=1360s", Post_live="True", User_id=1, Person="Noam Chomsky")
    modules.INSERT_POST(Post_title="Noam Chomsky Ukraine 2 TALK6", Post_description="here is noam chomsky philosopher talking about x", Post_link="https://www.youtube.com/watch?v=aiJEmB3wBxM",Post_live="True", User_id=1, Person="Noam Chomsky")
    
    # PETER THIEL DEMO
    modules.INSERT_POST(Post_title="Peter Thiel X talk1", Post_description="here is peter thiel philosopher talking about x", Post_link="https://www.youtube.com/watch?v=XvKi7Omg1_M",Post_live="True", User_id=1, Person="Peter Thiel")
    modules.INSERT_POST(Post_title="Peter Thiel X talk2", Post_description="here is peter thiel philosopher talking about x", Post_link="https://www.youtube.com/watch?v=qYSnVR7d4VE",Post_live="True", User_id=1, Person="Peter Thiel")
    modules.INSERT_POST(Post_title="Peter Thiel X talk3", Post_description="here is peter thiel philosopher talking about x", Post_link="https://www.youtube.com/watch?v=F3EBfS9IcB4&t=2518s",Post_live="True", User_id=1, Person="Peter Thiel")
    modules.INSERT_POST(Post_title="Peter Thiel X talk4", Post_description="here is peter thiel philosopher talking about x", Post_link="https://www.youtube.com/watch?v=3Fx5Q8xGU8k&t=2553s",Post_live="True", User_id=1, Person="Peter Thiel") 
    modules.INSERT_POST(Post_title="SPOTIFY Peter Thiel X talk", Post_description="here is peter thiel philosopher talking about x", Post_link="https://open.spotify.com/episode/4CESb99rKgkQ5MvNL4HaFJ?si=3e1ea553d7c14637", Post_live="True", User_id=1, Person="Peter Thiel") 
    modules.INSERT_POST(Post_title="tiktok Peter Thiel X talk", Post_description="here is peter thiel philosopher talking about x", Post_link="https://www.tiktok.com/@mazinosarchive/video/7177147474233150726?is_copy_url=1&is_from_webapp=v1",Post_live="True", User_id=1, Person="Peter Thiel")
    
    modules.INSERT_POST(Post_title="rumble Peter Thiel X talk1", Post_description="here is peter thiel philosopher talking about x", Post_link="https://rumble.com/v10648s-paypal-co-founder-peter-thiel-bitcoin-keynote-bitcoin-2022-conference.html",Post_live="False", User_id=1, Person="Peter Thiel")
    modules.INSERT_POST(Post_title="rumble Peter Thiel X talk2", Post_description="here is peter thiel philosopher talking about x", Post_link="https://rumble.com/v1lr7qn-peter-thiel-3-.html",Post_live="False", User_id=1, Person="Peter Thiel")
    
    
    
    # MICHAEL SUGRUE DEMO
    modules.INSERT_POST(Post_title="Michael Sugrue X talk1", Post_description="here is michael sugrue philosopher talking about x", Post_link="https://www.youtube.com/watch?v=UlsR7_Wn8wc",Post_live="True", User_id=1, Person="Michael Sugrue")
    modules.INSERT_POST(Post_title="Michael Sugrue X talk2", Post_description="here is michael sugrue philosopher talking about x", Post_link="https://www.youtube.com/watch?v=_PSRVuQvVuU",Post_live="True", User_id=1, Person="Michael Sugrue")
    modules.INSERT_POST(Post_title="Michael Sugrue X talk3", Post_description="here is michael sugrue philosopher talking about x", Post_link="https://www.youtube.com/watch?v=WHiPfvzap3o",Post_live="True", User_id=1, Person="Michael Sugrue")
    modules.INSERT_POST(Post_title="Michael Sugrue X talk4", Post_description="here is michael sugrue philosopher talking about x", Post_link="https://www.youtube.com/watch?v=tyb93qZIC7g&t=1556s",Post_live="True", User_id=1, Person="Michael Sugrue") 

    # VERVAEKE DEMO
    modules.INSERT_POST(Post_title="John Vervaeke X talk1", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.youtube.com/watch?v=54l8_ewcOlY&t=1488s",Post_live="True", User_id=1, Person="John Vervaeke") 
    modules.INSERT_POST(Post_title="John Vervaeke talk2", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.youtube.com/watch?v=aF9HeXg65AE&t=71s",Post_live="True", User_id=1, Person="John Vervaeke") 
    modules.INSERT_POST(Post_title="John Vervaeke X talk3", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.youtube.com/watch?v=C1AaqD8t3pk",Post_live="True", User_id=1, Person="John Vervaeke") 
    modules.INSERT_POST(Post_title="John Vervaeke X talk4", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.youtube.com/watch?v=Lhl51bZQlM8",Post_live="True", User_id=1, Person="John Vervaeke") 
    modules.INSERT_POST(Post_title="John Vervaeke X talk5", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.youtube.com/watch?v=A_gH5VIZO0Q&t=158s",Post_live="True", User_id=1, Person="John Vervaeke") 
    modules.INSERT_POST(Post_title="John Vervaeke X talk6", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.youtube.com/watch?v=EWumJSBqXa8",Post_live="True", User_id=1, Person="John Vervaeke") 
    modules.INSERT_POST(Post_title="John Vervaeke X talk7", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.youtube.com/watch?v=39NpjQDtqNw",Post_live="True", User_id=1, Person="John Vervaeke") 
    modules.INSERT_POST(Post_title="John Vervaeke X talk8", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.youtube.com/watch?v=KoqibFwvQJ4",Post_live="True", User_id=1, Person="John Vervaeke") 
    modules.INSERT_POST(Post_title="John Vervaeke X talk9", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.youtube.com/watch?v=rpivf1SoEdc",Post_live="True", User_id=1, Person="John Vervaeke") 
    modules.INSERT_POST(Post_title="John Vervaeke X talk10", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.youtube.com/watch?v=hl2TE-mXPwM",Post_live="False", User_id=1, Person="John Vervaeke") 

    # MORE TESTS
    modules.INSERT_POST(Post_title="Balaji Srinivasan X talk1", Post_description="here is John VASDKJFHALSKDJFHervaeke philosopher talking about x", Post_link="https://www.tiktok.com/@mazinosarchive/video/7179325211559431429?is_copy_url=1&is_from_webapp=v1",Post_live="True", User_id=1, Person="Balaji Srinivasan") 
    modules.INSERT_POST(Post_title="Balaji Srinivasan X talk2", Post_description="here is John  VASDKJFHALSphilosopher talking about x", Post_link="https://www.tiktok.com/@mazinosarchive/video/7180911568014576902?is_copy_url=1&is_from_webapp=v1",Post_live="True", User_id=1, Person="Balaji Srinivasan") 
    modules.INSERT_POST(Post_title="Balaji Srinivasan X talk3", Post_description="here is John Ve VASDKJFHALSe philosopher talking about x", Post_link="https://www.tiktok.com/@mazinosarchive/video/7181499250176478469?is_copy_url=1&is_from_webapp=v1",Post_live="True", User_id=1, Person="Balaji Srinivasan") 
    modules.INSERT_POST(Post_title="Balaji Srinivasan X talk4", Post_description="here is Jo VASDKJFHALSphilosopher talking about x", Post_link="https://www.tiktok.com/@mazinosarchive/video/7181480403738430726?is_copy_url=1&is_from_webapp=v1",Post_live="True", User_id=1, Person="Balaji Srinivasan") 
    modules.INSERT_POST(Post_title="Balaji Srinivasan X talk5", Post_description="here is J VASDKJFHALSe philosopher talking about x", Post_link="https://www.tiktok.com/@mazinosarchive/video/7181480056470998278?is_copy_url=1&is_from_webapp=v1",Post_live="True", User_id=1, Person="Balaji Srinivasan") 
    modules.INSERT_POST(Post_title="Balaji Srinivasan X talk6", Post_description="here is Jo VASDKJFHALSe philosopher talking about x", Post_link="https://www.tiktok.com/@mazinosarchive/video/7181479698541628678?is_copy_url=1&is_from_webapp=v1",Post_live="True", User_id=1, Person="Balaji Srinivasan") 
    modules.INSERT_POST(Post_title="Balaji SrinivasanX talk7", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.tiktok.com/@mazinosarchive/video/7181479209515158790?is_copy_url=1&is_from_webapp=v1",Post_live="True", User_id=1, Person="Balaji Srinivasan") 
    modules.INSERT_POST(Post_title="Balaji Srinivasan X talk8", Post_description="here is John VASDKJFHALSilosopher talking about x", Post_link="https://www.tiktok.com/@mazinosarchive/video/7180909636139109638?is_copy_url=1&is_from_webapp=v1",Post_live="True", User_id=1, Person="Balaji Srinivasan") 
    modules.INSERT_POST(Post_title="Balaji Srinivasan X talk0", Post_description="here is Joh VASDKJFHALSlosopher talking about x", Post_link="https://www.tiktok.com/@mazinosarchive/video/7180909285420010758?is_copy_url=1&is_from_webapp=v1",Post_live="True", User_id=1, Person="Balaji Srinivasan") 
    modules.INSERT_POST(Post_title="Balaji Srinivasan X talk6182", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.tiktok.com/@mazinosarchive/video/7181154493080308998?is_copy_url=1&is_from_webapp=v1",Post_live="True", User_id=1, Person="Balaji Srinivasan") 

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
    

def INSERT_DEMO_TRIBUNAL_WORD_VOTE():
    modules.INSERT_INTO_PROFANITY_LIST_VOTES(3, 1, "DOWN")
    modules.INSERT_INTO_PROFANITY_LIST_VOTES(3, 1, "DOWN")
    modules.INSERT_INTO_PROFANITY_LIST_VOTES(3, 1, "UP")
    modules.INSERT_INTO_PROFANITY_LIST_VOTES(3, 1, "UP")
    modules.INSERT_INTO_PROFANITY_LIST_VOTES(3, 1, "UP")
    modules.INSERT_INTO_PROFANITY_LIST_VOTES(3, 1, "UP")
    modules.INSERT_INTO_PROFANITY_LIST_VOTES(3, 1, "UP")
    modules.INSERT_INTO_PROFANITY_LIST_VOTES(3, 1, "UP")
        

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
    # modules.INSERT_REQUEST(User_id=1, Request_type="PERSON", Request_content="Steve Jobs")  
    
def FULL_DEMO_INSERT():
    INSERT_DEMO_USER()
    INSERT_DEMO_ADMIN()
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
    INSERT_DEMO_TRIBUNAL_WORD_VOTE()
    
    
if __name__ == "__main__":

    answer = input("DO YOU WANT TO REALLY RESET? [NOT IN SERVER]")
    if answer.lower() in ["y", "yes"]:
        modules.CREATE_TABLES("false")
        FULL_DEMO_INSERT()
