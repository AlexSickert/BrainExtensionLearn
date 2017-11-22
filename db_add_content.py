#!/usr/bin/env python

import psycopg2
import sys, traceback
import log

print("loading db_add_content.py")


def add_one_word(x):
    
    hostname = 'localhost'
    username = 'postgres'
    password = 'password'
    database = 'brainextension'

    log.log_info("111  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    try:
    
        conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )

        cur = conn.cursor()
        xxx = x
        yyy = x
        cur.execute( "insert into users (email, password) values (%s, %s);", (xxx,yyy) )
        # cur.execute("insert into user_1_languages (language) values (%s);", (xxx,))
        conn.commit()
        conn.close()

        log.log_info("222  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

        conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )

        cur = conn.cursor()

        # cur.execute( "SELECT id, language FROM user_1_languages;" )
        cur.execute("SELECT id, email FROM users;")

        log.log_info("333  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    except:

        log.log_info ("Exception in user code:")
        log.log_info ('-'*60)
        traceback.print_exc(file=sys.stdout)
        log.log_info ('-'*60)
  
#
#    for a, b in cur.fetchall() :
#        print(a)
#        print(b)
    for row in cur:
        log.log_info(row[0])
        log.log_info(row[1])
        
    conn.close()
    
    
    
    
    
    