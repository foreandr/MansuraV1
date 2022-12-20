try:    
    import python.MODULES as modules
except:
    import MODULES as modules

def CATEGORY_SEARCH(category_id):
    if category_id == "":
        return ""
    else:
        return F"AND cat.Category_id = '{category_id}'"