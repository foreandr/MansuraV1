import inspect
try:    
    import python.MODULES as modules
except:
    import MODULES as modules

def INSERT_DEMO_COMMENT_VOTE():
    modules.INSERT_COMMENT_VOTE(Comment_id=1, User_id=1)
    modules.INSERT_COMMENT_VOTE(Comment_id=1, User_id=1) 
    
    modules.INSERT_COMMENT_VOTE(Comment_id=2, User_id=1)
    modules.INSERT_COMMENT_VOTE(Comment_id=1, User_id=3)
    
    modules.INSERT_COMMENT_VOTE(Comment_id=1, User_id=1)
    modules.INSERT_COMMENT_VOTE(Comment_id=2, User_id=2)  

def INSERT_DEMO_USER():
    modules.print_title(f"{inspect.stack()[0][3]}")
    
    modules.INSERT_USER("Foreman", "helloWorld!", "andrfore@gmail.com")
    modules.INSERT_USER("David", "helloWorld!", "david@gmail.com")
    modules.INSERT_USER("Homer", "helloWorld!", "homer@gmail.com")
    modules.INSERT_USER("Simpson", "helloWorld!", "Simpson@gmail.com")
    modules.INSERT_USER("Goes", "helloWorld!", "Goes@gmail.com")
    modules.INSERT_USER("ToTheMoon", "helloWorld!", "ToTheMoon@gmail.com")
    modules.INSERT_USER("IEatBagels", "helloWorld!", "IEatBagels@gmail.com")
    modules.INSERT_USER("DonutCity", "helloWorld!", "DonutCity@gmail.com")
    
    modules.INSERT_USER("Foreman1", "helloWorld!", "Foreman1@gmail.com")
    modules.INSERT_USER("Foreman2", "helloWorld!", "Foreman2@gmail.com")
    modules.INSERT_USER("Foreman3", "helloWorld!", "Foreman3@gmail.com")
    modules.INSERT_USER("Foreman4", "helloWorld!", "Foreman4@gmail.com")
    modules.INSERT_USER("Foreman5", "helloWorld!", "Foreman5@gmail.com")
    modules.INSERT_USER("Foreman6", "helloWorld!", "Foreman6@gmail.com")
    modules.INSERT_USER("Foreman7", "helloWorld!", "Foreman7@gmail.com")
    modules.INSERT_USER("Foreman8", "helloWorld!", "Foreman8@gmail.com")
    modules.INSERT_USER("Foreman9", "helloWorld!", "Foreman9@gmail.com")
    
    modules.INSERT_USER("Foreman11", "helloWorld!", "Foreman11@gmail.com")
    modules.INSERT_USER("Foreman12", "helloWorld!", "Foreman12@gmail.com")
    modules.INSERT_USER("Foreman13", "helloWorld!", "Foreman13@gmail.com")
    modules.INSERT_USER("Foreman14", "helloWorld!", "Foreman14@gmail.com")
    modules.INSERT_USER("Foreman15", "helloWorld!", "Foreman15@gmail.com")
    modules.INSERT_USER("Foreman16", "helloWorld!", "Foreman16@gmail.com")
    modules.INSERT_USER("Foreman17", "helloWorld!", "Foreman17@gmail.com")
    modules.INSERT_USER("Foreman18", "helloWorld!", "Foreman18@gmail.com")
    modules.INSERT_USER("Foreman19", "helloWorld!", "Foreman19@gmail.com")
    
    modules.INSERT_USER("Foreman21", "helloWorld!", "Foreman21@gmail.com")
    modules.INSERT_USER("Foreman22", "helloWorld!", "Foreman22@gmail.com")
    modules.INSERT_USER("Foreman23", "helloWorld!", "Foreman23@gmail.com")
    modules.INSERT_USER("Foreman24", "helloWorld!", "Foreman24@gmail.com")
    modules.INSERT_USER("Foreman25", "helloWorld!", "Foreman25@gmail.com")
    modules.INSERT_USER("Foreman26", "helloWorld!", "Foreman26@gmail.com")
    modules.INSERT_USER("Foreman27", "helloWorld!", "Foreman27@gmail.com")
    modules.INSERT_USER("Foreman28", "helloWorld!", "Foreman28@gmail.com")
    modules.INSERT_USER("Foreman29", "helloWorld!", "Foreman29@gmail.com")

    modules.INSERT_USER("Foreman31", "helloWorld!", "Foreman31@gmail.com")
    modules.INSERT_USER("Foreman32", "helloWorld!", "Foreman32@gmail.com")
    modules.INSERT_USER("Foreman33", "helloWorld!", "Foreman33@gmail.com")
    modules.INSERT_USER("Foreman34", "helloWorld!", "Foreman34@gmail.com")
    modules.INSERT_USER("Foreman35", "helloWorld!", "Foreman35@gmail.com")
    modules.INSERT_USER("Foreman36", "helloWorld!", "Foreman36@gmail.com")
    modules.INSERT_USER("Foreman37", "helloWorld!", "Foreman37@gmail.com")
    modules.INSERT_USER("Foreman38", "helloWorld!", "Foreman38@gmail.com")
    modules.INSERT_USER("Foreman39", "helloWorld!", "Foreman39@gmail.com")
    
    modules.INSERT_USER("Foreman41", "helloWorld!", "Foreman41@gmail.com")
    modules.INSERT_USER("Foreman42", "helloWorld!", "Foreman42@gmail.com")
    modules.INSERT_USER("Foreman43", "helloWorld!", "Foreman43@gmail.com")
    modules.INSERT_USER("Foreman44", "helloWorld!", "Foreman44@gmail.com")
    modules.INSERT_USER("Foreman45", "helloWorld!", "Foreman45@gmail.com")
    modules.INSERT_USER("Foreman46", "helloWorld!", "Foreman46@gmail.com")
    modules.INSERT_USER("Foreman47", "helloWorld!", "Foreman47@gmail.com")
    modules.INSERT_USER("Foreman48", "helloWorld!", "Foreman48@gmail.com")
    modules.INSERT_USER("Foreman49", "helloWorld!", "Foreman49@gmail.com")

    
def INSERT_DEMO_ADMIN():
    modules.INSERT_POST_ADMIN(1)
    modules.INSERT_POST_ADMIN(2)
       
def INSERT_DEMO_PEOPLE():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_PERSON("Noam Chomsky")
    modules.INSERT_PERSON("Peter Thiel")
    modules.INSERT_PERSON("Michael Sugrue")
    modules.INSERT_PERSON("John Vervaeke")
    modules.INSERT_PERSON("George Hotz")
    modules.INSERT_PERSON("Adina Samuels", Person_live="False")
    modules.INSERT_PERSON("Kristen Celotto", Person_live="False")

def INSERT_DEMO_POST():
    modules.print_title(f"{inspect.stack()[0][3]}")
    # CHOMSKY DEMO
    
    modules.INSERT_POST(Post_title="Noam Chomsky Ukraine 2 TALK2", Post_description="here is noam chomsky philosopher talking about x", Post_link="https://www.youtube.com/watch?v=J_jzFt8VLnk", Post_live="True", User_id=2, Person=["Noam Chomsky","Peter Thiel", "Michael Sugrue"])
    modules.INSERT_POST(Post_title="Noam Chomsky Ukraine 2 TALK3", Post_description="here is noam chomsky philosopher talking about x", Post_link="https://www.youtube.com/watch?v=2IWkSTrfBdU", Post_live="True", User_id=2, Person=["Noam Chomsky"])
    modules.INSERT_POST(Post_title="Noam Chomsky Ukraine 2 TALK4", Post_description="here is noam chomsky philosopher talking about x", Post_link="https://www.youtube.com/watch?v=w_X5czMVKT8", Post_live="True", User_id=2, Person=["Noam Chomsky"])
    modules.INSERT_POST(Post_title="Noam Chomsky Ukraine 2 TALK5", Post_description="here is noam chomsky philosopher talking about x", Post_link="https://www.youtube.com/watch?v=XNSxj0TVeJs&t=1360s", Post_live="True", User_id=2, Person=["Noam Chomsky"])
    modules.INSERT_POST(Post_title="Noam Chomsky Ukraine 2 TALK6", Post_description="here is noam chomsky philosopher talking about x", Post_link="https://www.youtube.com/watch?v=aiJEmB3wBxM",Post_live="True", User_id=2, Person=["Noam Chomsky"])
    #5
    # PETER THIEL DEMO
    modules.INSERT_POST(Post_title="Peter Thiel X talk1", Post_description="here is peter thiel philosopher talking about x", Post_link="https://www.youtube.com/watch?v=XvKi7Omg1_M",Post_live="True", User_id=2, Person=["Peter Thiel", "Noam Chomsky"])
    modules.INSERT_POST(Post_title="Peter Thiel X talk2", Post_description="here is peter thiel philosopher talking about x", Post_link="https://www.youtube.com/watch?v=qYSnVR7d4VE",Post_live="True", User_id=2, Person=["Peter Thiel"])
    modules.INSERT_POST(Post_title="Peter Thiel X talk3", Post_description="here is peter thiel philosopher talking about x", Post_link="https://www.youtube.com/watch?v=F3EBfS9IcB4&t=2518s",Post_live="True", User_id=3, Person=["Peter Thiel"])
    modules.INSERT_POST(Post_title="Peter Thiel X talk4", Post_description="here is peter thiel philosopher talking about x", Post_link="https://www.youtube.com/watch?v=3Fx5Q8xGU8k&t=2553s",Post_live="True", User_id=3, Person=["Peter Thiel"]) 
    modules.INSERT_POST(Post_title="SPOTIFY Peter Thiel X talk", Post_description="here is peter thiel philosopher talking about x", Post_link="https://open.spotify.com/episode/4CESb99rKgkQ5MvNL4HaFJ?si=3e1ea553d7c14637", Post_live="True", User_id=2, Person=["Peter Thiel"]) 
    #10
    """
    modules.INSERT_POST(Post_title="tiktok Peter Thiel X talk", Post_description="here is peter thiel philosopher talking about x", Post_link="https://www.tiktok.com/@mazinosarchive/video/7177147474233150726?is_copy_url=1&is_from_webapp=v1",Post_live="True", User_id=1, Person="Peter Thiel")
    
    modules.INSERT_POST(Post_title="rumble Peter Thiel X talk1", Post_description="here is peter thiel philosopher talking about x", Post_link="https://rumble.com/v10648s-paypal-co-founder-peter-thiel-bitcoin-keynote-bitcoin-2022-conference.html",Post_live="False", User_id=1, Person="Peter Thiel")
    modules.INSERT_POST(Post_title="rumble Peter Thiel X talk2", Post_description="here is peter thiel philosopher talking about x", Post_link="https://rumble.com/v1lr7qn-peter-thiel-3-.html",Post_live="False", User_id=1, Person="Peter Thiel")
    """
    
    
    # MICHAEL SUGRUE DEMO
    modules.INSERT_POST(Post_title="Michael Sugrue X talk1", Post_description="here is michael sugrue philosopher talking about x", Post_link="https://www.youtube.com/watch?v=UlsR7_Wn8wc",Post_live="True", User_id=2, Person=["Michael Sugrue"])
    modules.INSERT_POST(Post_title="Michael Sugrue X talk2", Post_description="here is michael sugrue philosopher talking about x", Post_link="https://www.youtube.com/watch?v=_PSRVuQvVuU",Post_live="True", User_id=2, Person=["Michael Sugrue"])
    modules.INSERT_POST(Post_title="Michael Sugrue X talk3", Post_description="here is michael sugrue philosopher talking about x", Post_link="https://www.youtube.com/watch?v=WHiPfvzap3o",Post_live="True", User_id=2, Person=["Michael Sugrue"])
    modules.INSERT_POST(Post_title="Michael Sugrue X talk4", Post_description="here is michael sugrue philosopher talking about x", Post_link="https://www.youtube.com/watch?v=tyb93qZIC7g&t=1556s",Post_live="True", User_id=2, Person=["Michael Sugrue"]) 
    #14
    # VERVAEKE DEMO
    modules.INSERT_POST(Post_title="John Vervaeke X talk1", Post_description="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", Post_link="https://www.youtube.com/watch?v=54l8_ewcOlY&t=1488s",Post_live="True", User_id=1, Person=["John Vervaeke"]) 
    modules.INSERT_POST(Post_title="John Vervaeke talk2", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.youtube.com/watch?v=aF9HeXg65AE&t=71s",Post_live="True", User_id=3, Person=["John Vervaeke"]) 
    modules.INSERT_POST(Post_title="John Vervaeke X talk3", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.youtube.com/watch?v=C1AaqD8t3pk",Post_live="True", User_id=3, Person=["John Vervaeke"]) 
    modules.INSERT_POST(Post_title="John Vervaeke X talk4", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.youtube.com/watch?v=Lhl51bZQlM8",Post_live="True", User_id=3, Person=["John Vervaeke"]) 
    modules.INSERT_POST(Post_title="John Vervaeke X talk5", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.youtube.com/watch?v=A_gH5VIZO0Q&t=158s",Post_live="True", User_id=1, Person=["John Vervaeke"]) 
    modules.INSERT_POST(Post_title="John Vervaeke X talk6", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.youtube.com/watch?v=EWumJSBqXa8",Post_live="True", User_id=3, Person=["John Vervaeke"]) 
    modules.INSERT_POST(Post_title="John Vervaeke X talk7", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.youtube.com/watch?v=39NpjQDtqNw",Post_live="True", User_id=3, Person=["John Vervaeke"]) 
    modules.INSERT_POST(Post_title="John Vervaeke X talk8", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.youtube.com/watch?v=KoqibFwvQJ4",Post_live="True", User_id=3, Person=["John Vervaeke"]) 
    modules.INSERT_POST(Post_title="John Vervaeke X talk9", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.youtube.com/watch?v=rpivf1SoEdc",Post_live="True", User_id=3, Person=["John Vervaeke"]) 
    modules.INSERT_POST(Post_title="John Vervaeke X talk10", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.youtube.com/watch?v=hl2TE-mXPwM",Post_live="False", User_id=1, Person=["John Vervaeke"]) 
    #24
    # MORE TESTS
    
    modules.INSERT_POST(Post_title="Balaji Srinivasan X talk1", Post_description="here is John VASDKJFHALSKDJFHervaeke philosopher talking about x", Post_link="https://www.tiktok.com/@mazinosarchive/video/7179325211559431429?is_copy_url=1&is_from_webapp=v1",Post_live="True", User_id=1, Person=["Balaji Srinivasan"]) 
    modules.INSERT_POST(Post_title="Balaji Srinivasan X talk2", Post_description="here is John  VASDKJFHALSphilosopher talking about x", Post_link="https://www.tiktok.com/@mazinosarchive/video/7180911568014576902?is_copy_url=1&is_from_webapp=v1",Post_live="True", User_id=1, Person=["Balaji Srinivasan"]) 
    modules.INSERT_POST(Post_title="Balaji Srinivasan X talk3", Post_description="here is John Ve VASDKJFHALSe philosopher talking about x", Post_link="https://www.tiktok.com/@mazinosarchive/video/7181499250176478469?is_copy_url=1&is_from_webapp=v1",Post_live="True", User_id=1, Person=["Balaji Srinivasan"]) 
    modules.INSERT_POST(Post_title="Balaji Srinivasan X talk4", Post_description="here is Jo VASDKJFHALSphilosopher talking about x", Post_link="https://www.tiktok.com/@mazinosarchive/video/7181480403738430726?is_copy_url=1&is_from_webapp=v1",Post_live="True", User_id=1, Person=["Balaji Srinivasan"]) 
    modules.INSERT_POST(Post_title="Balaji Srinivasan X talk5", Post_description="here is J VASDKJFHALSe philosopher talking about x", Post_link="https://www.tiktok.com/@mazinosarchive/video/7181480056470998278?is_copy_url=1&is_from_webapp=v1",Post_live="True", User_id=1, Person=["Balaji Srinivasan"]) 
    modules.INSERT_POST(Post_title="Balaji Srinivasan X talk6", Post_description="here is Jo VASDKJFHALSe philosopher talking about x", Post_link="https://www.tiktok.com/@mazinosarchive/video/7181479698541628678?is_copy_url=1&is_from_webapp=v1",Post_live="True", User_id=1, Person=["Balaji Srinivasan"]) 
    modules.INSERT_POST(Post_title="Balaji SrinivasanX talk7", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.tiktok.com/@mazinosarchive/video/7181479209515158790?is_copy_url=1&is_from_webapp=v1",Post_live="True", User_id=1, Person=["Balaji Srinivasan"]) 
    modules.INSERT_POST(Post_title="Balaji Srinivasan X talk8", Post_description="here is John VASDKJFHALSilosopher talking about x", Post_link="https://www.tiktok.com/@mazinosarchive/video/7180909636139109638?is_copy_url=1&is_from_webapp=v1",Post_live="True", User_id=1, Person=["Balaji Srinivasan"]) 
    modules.INSERT_POST(Post_title="Balaji Srinivasan X talk0", Post_description="here is Joh VASDKJFHALSlosopher talking about x", Post_link="https://www.tiktok.com/@mazinosarchive/video/7180909285420010758?is_copy_url=1&is_from_webapp=v1",Post_live="True", User_id=1, Person=["Balaji Srinivasan"]) 
    modules.INSERT_POST(Post_title="Balaji Srinivasan X talk6182", Post_description="here is John Vervaeke philosopher talking about x", Post_link="https://www.tiktok.com/@mazinosarchive/video/7181154493080308998?is_copy_url=1&is_from_webapp=v1",Post_live="True", User_id=1, Person=["Balaji Srinivasan"]) 

    
    modules.INSERT_POST(Post_title="George Hotz title post1", Post_description="here is George Hotz philosopher talking about x", Post_link="https://www.youtube.com/watch?v=hDkLoRyiIeI&t=65s",Post_live="True", User_id=1, Person=["George Hotz"]) 
    modules.INSERT_POST(Post_title="George Hotz title post2", Post_description="here is George Hotz philosopher talking about x", Post_link="https://www.youtube.com/watch?v=mBnBH8Ga9-w",Post_live="True", User_id=1, Person=["George Hotz"]) 
    modules.INSERT_POST(Post_title="George Hotz title post3", Post_description="here is George Hotz philosopher talking about x", Post_link="https://www.youtube.com/watch?v=-NleKOVsl28",Post_live="True", User_id=1, Person=["George Hotz"]) 
    modules.INSERT_POST(Post_title="George Hotz title post4", Post_description="here is George Hotz philosopher talking about x", Post_link="https://www.youtube.com/watch?v=nvtoOxNfDQo",Post_live="True", User_id=1, Person=["George Hotz"]) 
    modules.INSERT_POST(Post_title="George Hotz title post5", Post_description="here is George Hotz philosopher talking about x", Post_link="https://www.youtube.com/watch?v=KF7X7s48jRc",Post_live="True", User_id=1, Person=["George Hotz"]) 
    modules.INSERT_POST(Post_title="George Hotz title post6", Post_description="here is George Hotz philosopher talking about x", Post_link="https://www.youtube.com/watch?v=z6xslDMimME",Post_live="True", User_id=1, Person=["George Hotz"]) 
    modules.INSERT_POST(Post_title="George Hotz title post7", Post_description="here is George Hotz philosopher talking about x", Post_link="https://www.youtube.com/watch?v=_CP8d4nCnlw&t=5434s",Post_live="True", User_id=1, Person=["George Hotz"]) 
    modules.INSERT_POST(Post_title="George Hotz title post8", Post_description="here is George Hotz philosopher talking about x", Post_link="https://www.youtube.com/watch?v=9wQDMh3Lbjc&t=1773s",Post_live="True", User_id=1, Person=["George Hotz"]) 
    modules.INSERT_POST(Post_title="George Hotz title post9", Post_description="here is George Hotz philosopher talking about x", Post_link="https://www.youtube.com/watch?v=4V9VHt_YwFQ&t=4646s",Post_live="True", User_id=1, Person=["George Hotz"]) 
    modules.INSERT_POST(Post_title="George Hotz title post10", Post_description="here is George Hotz philosopher talking about x", Post_link="https://www.youtube.com/watch?v=-rYKtRI_sDQ",Post_live="True", User_id=1, Person=["George Hotz"]) 
    modules.INSERT_POST(Post_title="George Hotz title post11", Post_description="here is George Hotz philosopher talking about x", Post_link="https://www.youtube.com/watch?v=FUMNRJfOQPc&t=2240s",Post_live="True", User_id=1, Person=["George Hotz"]) 

def INSERT_DEMO_SUBJECTS():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_SUBJECTS(Subject_name="Science")
    modules.INSERT_SUBJECTS(Subject_name="Language")
    modules.INSERT_SUBJECTS(Subject_name="Art")
    modules.INSERT_SUBJECTS(Subject_name="Lacan")
    modules.INSERT_SUBJECTS(Subject_name="Deluze")

def INSERT_DEMO_SUBSCRIPTIONS():
    modules.INSERT_SUBSCRIBE(Person_id=1, User_id=1) 
    modules.INSERT_SUBSCRIBE(Person_id=2, User_id=1) 
    modules.INSERT_SUBSCRIBE(Person_id=3, User_id=1)    
    modules.INSERT_SUBSCRIBE(Person_id=4, User_id=1) 
    modules.INSERT_SUBSCRIBE(Person_id=5, User_id=1) 
    modules.INSERT_SUBSCRIBE(Person_id=6, User_id=1) 
    
    modules.INSERT_SUBSCRIBE(Person_id=1, User_id=2) 
    modules.INSERT_SUBSCRIBE(Person_id=2, User_id=2) 
    modules.INSERT_SUBSCRIBE(Person_id=3, User_id=2)    
    modules.INSERT_SUBSCRIBE(Person_id=4, User_id=2) 
    modules.INSERT_SUBSCRIBE(Person_id=5, User_id=2) 
    modules.INSERT_SUBSCRIBE(Person_id=6, User_id=2)

def INSERT_DEMO_POST_SUBJECTS():
    modules.INSERT_POST_SUBJECTS(Subject_id=1, Post_id=1)
    modules.INSERT_POST_SUBJECTS(Subject_id=2, Post_id=1)
    modules.INSERT_POST_SUBJECTS(Subject_id=3, Post_id=1)
    modules.INSERT_POST_SUBJECTS(Subject_id=4, Post_id=1)
    
    modules.INSERT_POST_SUBJECTS(Subject_id=1, Post_id=2)
    modules.INSERT_POST_SUBJECTS(Subject_id=1, Post_id=3)
    modules.INSERT_POST_SUBJECTS(Subject_id=1, Post_id=4)
    
def INSERT_DEMO_LIKES():
    import random
     
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_LIKE(Post_id=1, User_id=1)
    modules.INSERT_LIKE(Post_id=2, User_id=1)
    modules.INSERT_LIKE(Post_id=3, User_id=1)
    modules.INSERT_LIKE(Post_id=4, User_id=1)
    modules.INSERT_LIKE(Post_id=5, User_id=1)
    modules.INSERT_LIKE(Post_id=6, User_id=1)
    modules.INSERT_LIKE(Post_id=7, User_id=1)
    modules.INSERT_LIKE(Post_id=8, User_id=1)
    modules.INSERT_LIKE(Post_id=9, User_id=1)
    modules.INSERT_LIKE(Post_id=10, User_id=1)
    modules.INSERT_LIKE(Post_id=11, User_id=1)
    modules.INSERT_LIKE(Post_id=12, User_id=1)
    modules.INSERT_LIKE(Post_id=13, User_id=1)
    modules.INSERT_LIKE(Post_id=14, User_id=1)
    modules.INSERT_LIKE(Post_id=15, User_id=1)
    modules.INSERT_LIKE(Post_id=16, User_id=1)
    modules.INSERT_LIKE(Post_id=17, User_id=1)
    modules.INSERT_LIKE(Post_id=18, User_id=1)
    modules.INSERT_LIKE(Post_id=19, User_id=1)
    modules.INSERT_LIKE(Post_id=20, User_id=1)
    modules.INSERT_LIKE(Post_id=21, User_id=1)
    modules.INSERT_LIKE(Post_id=22, User_id=1)
    modules.INSERT_LIKE(Post_id=23, User_id=1)
    
    for i in range(1, 35):
        for j in range(1,40):
            modules.INSERT_LIKE(Post_id=random.randint(j, 45), User_id=i)

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
    modules.INSERT_CONNECTION(user_id1=1, user_id2=1)
    modules.INSERT_CONNECTION(user_id1=2, user_id2=1)
    modules.INSERT_CONNECTION(user_id1=3, user_id2=1)
    modules.INSERT_CONNECTION(user_id1=4, user_id2=1)
    modules.INSERT_CONNECTION(user_id1=5, user_id2=1)
    modules.INSERT_CONNECTION(user_id1=6, user_id2=1)
    modules.INSERT_CONNECTION(user_id1=7, user_id2=1)
    modules.INSERT_CONNECTION(user_id1=8, user_id2=1)
    modules.INSERT_CONNECTION(user_id1=9, user_id2=1)
    modules.INSERT_CONNECTION(user_id1=10, user_id2=1)
    modules.INSERT_CONNECTION(user_id1=11, user_id2=1)
    modules.INSERT_CONNECTION(user_id1=12, user_id2=1)

    
    modules.INSERT_CONNECTION(user_id1=1, user_id2=2)
    modules.INSERT_CONNECTION(user_id1=2, user_id2=2)
    modules.INSERT_CONNECTION(user_id1=3, user_id2=2)
    modules.INSERT_CONNECTION(user_id1=4, user_id2=2)
    modules.INSERT_CONNECTION(user_id1=5, user_id2=2)
    modules.INSERT_CONNECTION(user_id1=6, user_id2=2)
    modules.INSERT_CONNECTION(user_id1=7, user_id2=2)
    modules.INSERT_CONNECTION(user_id1=8, user_id2=2)
    modules.INSERT_CONNECTION(user_id1=9, user_id2=2)
    modules.INSERT_CONNECTION(user_id1=10, user_id2=2)

    modules.INSERT_CONNECTION(user_id1=16, user_id2=2)
    modules.INSERT_CONNECTION(user_id1=17, user_id2=2)
    modules.INSERT_CONNECTION(user_id1=18, user_id2=2)
    modules.INSERT_CONNECTION(user_id1=19, user_id2=2)
    modules.INSERT_CONNECTION(user_id1=20, user_id2=2)
    
    modules.INSERT_CONNECTION(user_id1=1, user_id2=3)
    modules.INSERT_CONNECTION(user_id1=2, user_id2=3)
    modules.INSERT_CONNECTION(user_id1=3, user_id2=3)
    modules.INSERT_CONNECTION(user_id1=4, user_id2=3)
    modules.INSERT_CONNECTION(user_id1=5, user_id2=3)
    modules.INSERT_CONNECTION(user_id1=6, user_id2=3)
    modules.INSERT_CONNECTION(user_id1=7, user_id2=3)
    modules.INSERT_CONNECTION(user_id1=8, user_id2=3)
    modules.INSERT_CONNECTION(user_id1=9, user_id2=3)
    modules.INSERT_CONNECTION(user_id1=10, user_id2=3)
    modules.INSERT_CONNECTION(user_id1=11, user_id2=3)
    modules.INSERT_CONNECTION(user_id1=12, user_id2=3)

    modules.INSERT_CONNECTION(user_id1=16, user_id2=3)
    modules.INSERT_CONNECTION(user_id1=17, user_id2=3)
    modules.INSERT_CONNECTION(user_id1=18, user_id2=3)
    modules.INSERT_CONNECTION(user_id1=19, user_id2=3)
    modules.INSERT_CONNECTION(user_id1=20, user_id2=3)
    
    modules.INSERT_CONNECTION(user_id1=1, user_id2=4)
    modules.INSERT_CONNECTION(user_id1=2, user_id2=4)
    modules.INSERT_CONNECTION(user_id1=3, user_id2=4)
    modules.INSERT_CONNECTION(user_id1=4, user_id2=4)
    modules.INSERT_CONNECTION(user_id1=5, user_id2=4)
    modules.INSERT_CONNECTION(user_id1=6, user_id2=4)
    modules.INSERT_CONNECTION(user_id1=7, user_id2=4)
    modules.INSERT_CONNECTION(user_id1=8, user_id2=4)
    modules.INSERT_CONNECTION(user_id1=9, user_id2=4)
    modules.INSERT_CONNECTION(user_id1=10, user_id2=4)
    modules.INSERT_CONNECTION(user_id1=11, user_id2=4)
    modules.INSERT_CONNECTION(user_id1=12, user_id2=4)
    modules.INSERT_CONNECTION(user_id1=13, user_id2=4)
    modules.INSERT_CONNECTION(user_id1=14, user_id2=4)
    modules.INSERT_CONNECTION(user_id1=15, user_id2=4)
    modules.INSERT_CONNECTION(user_id1=16, user_id2=4)
    modules.INSERT_CONNECTION(user_id1=17, user_id2=4)
    modules.INSERT_CONNECTION(user_id1=18, user_id2=4)
    modules.INSERT_CONNECTION(user_id1=19, user_id2=4)
    modules.INSERT_CONNECTION(user_id1=20, user_id2=4)
    modules.INSERT_CONNECTION(user_id1=21, user_id2=4)
    modules.INSERT_CONNECTION(user_id1=22, user_id2=4)
    modules.INSERT_CONNECTION(user_id1=23, user_id2=4)
    modules.INSERT_CONNECTION(user_id1=24, user_id2=4)
    modules.INSERT_CONNECTION(user_id1=25, user_id2=4)
    modules.INSERT_CONNECTION(user_id1=26, user_id2=4)
    modules.INSERT_CONNECTION(user_id1=27, user_id2=4)
    modules.INSERT_CONNECTION(user_id1=28, user_id2=4)
    
    
    modules.INSERT_CONNECTION(user_id1=1, user_id2=6)
    modules.INSERT_CONNECTION(user_id1=2, user_id2=6)
    modules.INSERT_CONNECTION(user_id1=3, user_id2=6)
    modules.INSERT_CONNECTION(user_id1=4, user_id2=6)
    modules.INSERT_CONNECTION(user_id1=5, user_id2=6)
    modules.INSERT_CONNECTION(user_id1=6, user_id2=6)
    modules.INSERT_CONNECTION(user_id1=7, user_id2=6)
    modules.INSERT_CONNECTION(user_id1=8, user_id2=6)
    modules.INSERT_CONNECTION(user_id1=9, user_id2=6)
    modules.INSERT_CONNECTION(user_id1=10, user_id2=6)
    modules.INSERT_CONNECTION(user_id1=11, user_id2=6)
    modules.INSERT_CONNECTION(user_id1=12, user_id2=6)
    modules.INSERT_CONNECTION(user_id1=13, user_id2=6)
    modules.INSERT_CONNECTION(user_id1=14, user_id2=6)
    modules.INSERT_CONNECTION(user_id1=15, user_id2=6)
    modules.INSERT_CONNECTION(user_id1=16, user_id2=6)
    modules.INSERT_CONNECTION(user_id1=17, user_id2=6)
    modules.INSERT_CONNECTION(user_id1=18, user_id2=6)
    modules.INSERT_CONNECTION(user_id1=19, user_id2=6)
    modules.INSERT_CONNECTION(user_id1=20, user_id2=6)
    
    modules.INSERT_CONNECTION(user_id1=1, user_id2=9)
    modules.INSERT_CONNECTION(user_id1=13, user_id2=9)
    modules.INSERT_CONNECTION(user_id1=14, user_id2=9)
    modules.INSERT_CONNECTION(user_id1=15, user_id2=9)
    modules.INSERT_CONNECTION(user_id1=16, user_id2=9)
    modules.INSERT_CONNECTION(user_id1=17, user_id2=9)
    modules.INSERT_CONNECTION(user_id1=18, user_id2=9)
    modules.INSERT_CONNECTION(user_id1=19, user_id2=9)
    modules.INSERT_CONNECTION(user_id1=20, user_id2=9)
    
    modules.INSERT_CONNECTION(user_id1=1, user_id2=12)
    modules.INSERT_CONNECTION(user_id1=2, user_id2=12)

    
    modules.INSERT_CONNECTION(user_id1=1, user_id2=15)
    modules.INSERT_CONNECTION(user_id1=2, user_id2=15)
    modules.INSERT_CONNECTION(user_id1=3, user_id2=15)
    modules.INSERT_CONNECTION(user_id1=4, user_id2=15)
    modules.INSERT_CONNECTION(user_id1=5, user_id2=15)
    modules.INSERT_CONNECTION(user_id1=6, user_id2=15)
    modules.INSERT_CONNECTION(user_id1=7, user_id2=15)
    modules.INSERT_CONNECTION(user_id1=8, user_id2=15)
    modules.INSERT_CONNECTION(user_id1=9, user_id2=15)
    modules.INSERT_CONNECTION(user_id1=10, user_id2=15)
    modules.INSERT_CONNECTION(user_id1=11, user_id2=15)
    modules.INSERT_CONNECTION(user_id1=12, user_id2=15)
    modules.INSERT_CONNECTION(user_id1=13, user_id2=15)
    modules.INSERT_CONNECTION(user_id1=14, user_id2=15)
    modules.INSERT_CONNECTION(user_id1=15, user_id2=15)
    modules.INSERT_CONNECTION(user_id1=16, user_id2=15)

    
    modules.INSERT_CONNECTION(user_id1=1, user_id2=20)
    modules.INSERT_CONNECTION(user_id1=2, user_id2=20)
    modules.INSERT_CONNECTION(user_id1=3, user_id2=20)
    modules.INSERT_CONNECTION(user_id1=4, user_id2=20)
    modules.INSERT_CONNECTION(user_id1=5, user_id2=20)
    modules.INSERT_CONNECTION(user_id1=6, user_id2=20)
    modules.INSERT_CONNECTION(user_id1=7, user_id2=20)
    modules.INSERT_CONNECTION(user_id1=8, user_id2=20)
    modules.INSERT_CONNECTION(user_id1=9, user_id2=20)
    modules.INSERT_CONNECTION(user_id1=10, user_id2=20)
    modules.INSERT_CONNECTION(user_id1=11, user_id2=20)
    modules.INSERT_CONNECTION(user_id1=12, user_id2=20)
    modules.INSERT_CONNECTION(user_id1=13, user_id2=20)

    
def INSERT_DEMO_BLOCKS():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_BLOCKS(user_id1=3, user_id2=1)

def INSERT_DEMO_IP_ADRESSES():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_IP_ADRESSES(Address="0.0.0.0", User_id=1)
    modules.INSERT_IP_ADRESSES(Address="localhost", User_id=1)

def INSERT_DEMO_CHAT_MESSAGES():
    modules.INSERT_CHAT_MESSAGE(User_id=1, Room_id=1, Message="MESSAGE1")
    modules.INSERT_CHAT_MESSAGE(User_id=1, Room_id=1, Message="MESSAGE2")
    modules.INSERT_CHAT_MESSAGE(User_id=1, Room_id=1, Message="MESSAGE3")
    modules.INSERT_CHAT_MESSAGE(User_id=1, Room_id=1, Message="MESSAGE4")
    modules.INSERT_CHAT_MESSAGE(User_id=1, Room_id=1, Message="MESSAGE5")
    modules.INSERT_CHAT_MESSAGE(User_id=1, Room_id=1, Message="MESSAGE6")
    modules.INSERT_CHAT_MESSAGE(User_id=1, Room_id=1, Message="MESSAGE7")

def DEMO_CREATE_INITIAL_CHAT_ROOM():
    modules.INSERT_CHAT_ROOMS(Creator_id=1, Room_name="Homeroom",list_of_names=["Andre"])
    print("working")
    
def INSERT_DEMO_CHAT_ROOMS():
    modules.print_title(f"{inspect.stack()[0][3]}")
    
    modules.INSERT_CHAT_ROOMS(Creator_id=1, Room_name="hello world2",list_of_names=["Andre", "Foreman"])
    modules.INSERT_CHAT_ROOMS(Creator_id=2, Room_name="hello world3",list_of_names=["Andre", "David"])
    modules.INSERT_CHAT_ROOMS(Creator_id=3, Room_name="hello world4",list_of_names=["Andre", "David", "Foreman"])
    modules.INSERT_CHAT_ROOMS(Creator_id=3, Room_name="hello world5",list_of_names=["Andre", "David"])
    modules.INSERT_CHAT_ROOMS(Creator_id=3, Room_name="hello world6",list_of_names=["Andre"])
    
def INSERT_DEMO_CHAT_ROOMS_USER():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_CHAT_ROOMS_USER(User_id=1, Room_id=1)

def INSERT_DEMO_CHAT_ROOMS_ADMIN():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_CHAT_ROOMS_ADMIN(User_id=1, Room_id=1)

def INSERT_DEMO_REQUEST():
    modules.print_title(f"{inspect.stack()[0][3]}")
    # modules.INSERT_REQUEST(User_id=1, Request_type="PERSON", Request_content="Steve Jobs")  

def INSERT_DEMO_SEARCH_ALGO():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_SEARCH_ALGORITHM(Search_algorithm_name="Andre-Default", Search_where_clause="AND 1=1", Search_order_clause="""(SELECT COUNT(*) FROM FAVOURITES favourites WHERE favourites.Post_id = posts.Post_id)DESC,(SELECT COUNT(*) FROM FAVOURITES favourites WHERE favourites.Post_id = posts.Post_id )DESC,(SELECT COUNT(*) FROM VIEWS views WHERE views.Post_id = posts.Post_id) DESC, posts.Post_title""", User_id=1)
    
def INSERT_DEMO_SEARCH_VOTE():
    modules.print_title(f"{inspect.stack()[0][3]}")
    modules.INSERT_SEARCH_VOTE(Search_algorithm_id=1, User_id=1)

def FULL_DEMO_INSERT():
    modules.INSERT_USER("Andre", "helloWorld!", "foreandr@gmail.com")
    modules.INSERT_USER("Trial", "helloWorld!", "trial@gmail.com")
    DEMO_CREATE_INITIAL_CHAT_ROOM()
    
    INSERT_DEMO_USER()
    INSERT_DEMO_CHAT_ROOMS()
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
    # INSERT_DEMO_CHAT_ROOMS_USER()
    INSERT_DEMO_CHAT_ROOMS_ADMIN()
    INSERT_DEMO_REQUEST()
    INSERT_DEMO_TRIBUNAL_WORD_VOTE()
    INSERT_DEMO_SEARCH_ALGO()
    INSERT_DEMO_SEARCH_VOTE()
    INSERT_DEMO_CHAT_MESSAGES()
    
    
if __name__ == "__main__":

    answer = input("DO YOU WANT TO REALLY RESET? [NOT IN SERVER]")
    if answer.lower() in ["y", "yes"]:
        modules.CREATE_TABLES("false")
        FULL_DEMO_INSERT()
