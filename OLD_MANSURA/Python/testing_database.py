from itertools import pairwise
import psycopg2
import random
import os
import csv
import json
from db_connection import *
import helpers as helpers

conn = test_connection()
cursor = conn.cursor()


def test_connection():
    global conn
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="mansura",
            user="postgres",
            password="cooldood")
        # print("MySQL Database connection successful")
    except psycopg2.Error as err:
        print(f"Error: '{err}'")
    return conn



'''
((SELECT COUNT(*) FROM DISLIKES dislikes WHERE dislikes.File_id = F.File_id) / ((SELECT COUNT(*) FROM DISLIKES dislikes WHERE dislikes.File_id = F.File_id) + (SELECT COUNT(*) FROM LIKES likes WHERE likes.File_id = F.File_id))) > .75
(SELECT COUNT(*) FROM DISLIKES dislikes WHERE dislikes.File_id = F.File_id) > 10
'''
def CHECK_IF_FILE_FAILS_TRIBUNAL(file):
    conn = test_connection()
    cursor = conn.cursor()
    
    cursor.execute(f"""
        SELECT *
        FROM FILES file
        
        INNER JOIN TRIBUNAL trib
        ON trib.File_Id = file.File_id      
        
        WHERE file.File_id = {file}      
    """)
    exists = False
    for i in cursor.fetchall(): # INTERESTING LIL TRICK, IF IT'S EMPTY FALSE WILL RETURN 
        exists = True
                
    cursor.close()
    conn.close()
    return exists
        
  
def GET_ALL_REPORTS_FOR_POST(file_id):
    conn = test_connection()
    cursor = conn.cursor()
    
    cursor.execute(f"""
        SELECT * 
        FROM FILES file 
        
        INNER JOIN TRIBUNAL trib
        ON trib.File_id = trib.File_id
        
        -- WHERE trib.file_id = '{file_id}'              
    """)
    for i in cursor.fetchall(): # INTERESTING LIL TRICK, IF IT'S EMPTY FALSE WILL RETURN 
        print(i)
    
    cursor.close()
    conn.close()


def GIANT_TRIBUNAL_INSERT():
    f = open("names.txt", "r")
    Lines = f.readlines()
    
    count = 0
    
    with open('TEST_STRING_DEMO.txt', 'a') as f:
        f.write(F'\n\ndef GIANT_TRIBUNAL_INSERT():\n')
    mylist = ["EQUAL DISTRIBUTION", "LOG DISTRIBUTION"]
    for line in Lines:
        count += 1
        # print("Line{}: {}".format(count, line.strip()))
        name = line.strip()
        my_string = (f"""\tDB.TRIBUNAL_INSERT({random.randint(1, 100)}, {name})""")
        
        with open('TEST_STRING_DEMO.txt', 'a') as f:
            f.write(F'{my_string}\n')
GIANT_TRIBUNAL_INSERT()

# print(CHECK_IF_FILE_FAILS_TRIBUNAL(4))
#GET_ALL_REPORTS_FOR_POST(4)