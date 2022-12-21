try:    
    import python.MODULES as modules
except:
    import MODULES as modules

def CATEGORY_SEARCH(person_id):
    if person_id == "":
        return ""
    else:
        return F"AND person.Person_id = '{person_id}'"