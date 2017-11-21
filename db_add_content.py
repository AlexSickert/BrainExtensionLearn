#!/usr/bin/env python

import psycopg2

print("loading db_add_content.py")


def add_one_word(x):
    
    hostname = 'localhost'
    username = 'testuser'
    password = 'password'
    database = 'brainextension'
    
    conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    
    cur = conn.cursor()
    xxx = x
    cur.execute( "insert into user_1_languages (language) values (%s);", (xxx,) )
    conn.commit()
    conn.close()
    
    conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
        
    cur = conn.cursor()

    cur.execute( "SELECT id, language FROM user_1_languages;" )
    
  
#
#    for a, b in cur.fetchall() :
#        print(a)
#        print(b)
    for row in cur:
        print(row[0])
        print(row[1])
        
    conn.close()
    
    
    
    
    
    