#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 22:20:16 2017

@author: alex
"""

import psycopg2

from datetime import datetime





hostname = 'localhost'
username = 'testuser'
password = 'password'
database = 'brainextension'

#------------------------------------------------------------------------------
# Simple routine to run a query on a database and print the results:
def doQuery( conn ) :
    cur = conn.cursor()

    cur.execute( "SELECT id, language FROM user_1_languages" )
    

    for a, b in cur.fetchall() :
        print(a)
        print(b)

#------------------------------------------------------------------------------
def doInsert( conn ) :
    cur = conn.cursor()
    xxx = "O'Reilly"
    cur.execute( "insert into user_1_languages (language) values (%s)", (xxx,) )
    #cur.execute( "insert into user_1_languages (language) values (%s)", "123" )
    # see http://www.psycopg.org/psycopg/docs/usage.html#passing-parameters-to-sql-queries
    
    conn.commit()
    
    
    
#------------------------------------------------------------------------------
def doDelete( conn ) :
    cur = conn.cursor()
    xxx = "Chinese"
    cur.execute( "delete from user_1_languages where language =  %s", (xxx,) )
    #cur.execute( "delete from user_1_languages where language =  %s", "xxx" )
    # see http://www.psycopg.org/psycopg/docs/usage.html#passing-parameters-to-sql-queries
    
#------------------------------------------------------------------------------

def doInsertTimestamp( conn ) :

    cur = conn.cursor()
    dt = datetime.now()
    xxx = "O'Reilly"
    cur.execute( "insert into user_1_languages (language) values (%s)", (xxx,) )  
    #cur.execute( "insert into user_1_languages (language) values (%s)", "xxxx" )    
    #cur.execute('INSERT INTO some_table (somecol) VALUES (%s)', (dt,))




#------------------------------------------------------------------------------


myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
doInsertTimestamp( myConnection )
doInsert( myConnection )
doDelete( myConnection )
doInsert( myConnection )
doQuery( myConnection )
myConnection.close()
