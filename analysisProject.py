#!/usr/bin/env python

import psycopg2
DBName="news"

#def connect(dbname="news"):
def connect():
    """Connect to the PostgreSQL database"""
    try:
        db = psycopg2.connect(database=DBName)
        c = db.cursor()
        return db, c    
    except psycopg2.Error as e:
        print("Unable to connect database" + e.pgerror)

def view_popular_articles():
    try:
        db, c = connect()
        query = "create or replace view popular_articles as\
        select title, count(title) as views from articles, log\
        where concat('/article/',articles.slug) = log.path\
        group by title order by views desc"
        c.execute(query)
        db.commit()
        db.close()
    except psycopg2.Error as e:
        print("There is an error in creating view popular_articles " + e.pgerror)

def view_popular_authors():
    try:
        db, c = connect()
        query= "create or replace view popular_authors as select authors.name,\
        count(articles.author) as views from articles, authors, log\
        where concat('/article/',articles.slug) = log.path and articles.author = authors.id\
        group by authors.name order by views desc"
        c.execute(query)
        db.commit()
        db.close()
    except psycopg2.Error as e:
        print("There is an error in creating view popular_authors " + e.pgerror)

def view_log_errors():
    try:
        db, c = connect()
        query = "create or replace view log_errors as select Date, Total_Views, Total_Error,\
        (Total_Error::float*100)/Total_Views::float as Percent from\
        (select time::date as Date, count(status) as Total_Views,\
        sum(case when status = '404 NOT FOUND' then 1 else 0 end) as Total_Error\
        from log group by time::date) as result\
        where (Total_Error::float*100)/Total_Views::float > 1.0 order by Percent desc;"
        c.execute(query)
        db.commit()
        db.close()
    except psycopg2.Error as e:
        print("There is an error in creating view log_errors " + e.pgerror)

def popular_articles():
    """Print most popular three articles of all time"""
    count = 1		
    print ("1.The most popular three articles of the time:")	
    try:
        db, c = connect()
        query = "select * from popular_articles limit 3"
        c.execute(query)
        result = c.fetchall()
        db.close()      
    except psycopg2.Error as e:
        print("There is an error in calling module popular_articles" + e.pgerror)     
    for i in result:
        print str(count) + ") " + "\""  + i[0] + "\" - " + str(i[1]) + " views "  
        count += 1  
        	
def popular_authors():
    """Print most popular article authors of all time"""
    print ("\n2.The most popular article authors of the time:")
    try:
        db, c = connect()
        query = "select * from popular_authors"
        c.execute(query)
        result = c.fetchall()
        db.close()   
    except psycopg2.Error as e:
        print("There is an error in calling module popular_authors" + e.pgerror)
    for i in result:
        print "\"" + i[0] + "\" - " + str(i[1]) + " views "

def log_errors():
    """Print days on which more than 1% of requests lead to errors"""
    print ("\n3.Days with more than 1% of requests lead to errors:") 
    try:
        db, c = connect()
        query = "select * from log_status"
        c.execute(query)
        result = c.fetchall()
        db.close()   
    except psycopg2.Error as e:
        print("There is an error in calling module log_errors" + e.pgerror)  
    for i in result:
        print str(i[0])+ " - "+str(round(i[3], 2))+"% errors"

if __name__ == '__main__':
    # Call views    
    view_popular_articles()
    view_popular_authors()
    view_log_errors()
    
    # Call modules to print report 
    print "\nReporting results..."   
    popular_articles()
    popular_authors()
    log_errors()
   
    