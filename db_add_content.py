#!/usr/bin/env python

import psycopg2
import sys, traceback

print("loading db_add_content.py")


def add_one_word(x):
    
    hostname = 'localhost'
    username = 'postgres'
    password = 'password'
    database = 'brainextension'

    print("111  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    try:
    
        conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )

        cur = conn.cursor()
        xxx = x
        yyy = x
        cur.execute( "insert into users (email, password) values (%s, %s);", (xxx,yyy) )
        # cur.execute("insert into user_1_languages (language) values (%s);", (xxx,))
        conn.commit()
        conn.close()

        print("222  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

        conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )

        cur = conn.cursor()

        # cur.execute( "SELECT id, language FROM user_1_languages;" )
        cur.execute("SELECT id, email FROM users;")

        print("333  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    except:

        print ("Exception in user code:")
        print ('-'*60)
        traceback.print_exc(file=sys.stdout)
        print ('-'*60)
  
#
#    for a, b in cur.fetchall() :
#        print(a)
#        print(b)
    for row in cur:
        print(row[0])
        print(row[1])
        
    conn.close()
    
    
    
    
    
    