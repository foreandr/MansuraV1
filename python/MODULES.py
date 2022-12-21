'''
IF YOU EVER RUN INTO THE PROBLEM OF CIRCULAR IMPORTS,
GO TO THAT FILE AND JUST DO THE TRY EXCEPT FOR THE FILES THAT YOU NEED
'''
try:    
    from python.DB_CHECK import *
    from python.DB_CREATE import *
    from python.DB_DELETE import *
    from python.DB_READ import *
    from python.DB_INSERT import *
    from python.DB_UPDATE import *
    from python.DB_RESET import *
    from python.DB_SEARCH import *
    from python.DB_RECOVERY import *
    from python.DB_EMAIL import *
    from python.helpers import *
    from python.dbconnection import *
    from python.log import *
except:
    from DB_CHECK import *
    from DB_CREATE import *
    from DB_DELETE import *
    from DB_READ import *
    from DB_INSERT import *
    from DB_UPDATE import *
    from DB_RESET import *
    from DB_SEARCH import *
    from DB_RECOVERY import *
    from DB_EMAIL import *
    from helpers import *
    from dbconnection import *
    from log import *