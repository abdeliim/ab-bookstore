import os
import psycopg2
conn=psycopg2.connect("host=ec2-54-246-90-10.eu-west-1.compute.amazonaws.com dbname=d3lvkeb2pe1tju user=ojejhvdkytoheu password=e9fc09f3907c1fd2d9d9afc5b955e5ff392f42897c2f74b25c3bf4034fcc45d2")
cur=conn.cursor()
"""
cur.execute("""
    #CREATE TABLE books(#
    #isbn VARCHAR PRIMARY KEY NOT NULL,
    #title VARCHAR NOT NULL,
    #author VARCHAR NOT NULL,
    #year int NOT NULL
#)
""")

with open('books.csv', 'r') as f:    
    next(f) # Skip the header row.
    cur.copy_from(f, 'books', sep=',')

conn.commit()
"""
cur.execute("""
	CREATE TABLE users(
	name VARCHAR NOT NULL,
	username VARCHAR PRIMARY KEY NOT NULL,
	email VARCHAR NOT NULL,
	password VARCHAR NOT NULL)
	""")
conn.commit()