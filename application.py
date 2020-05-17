#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from flask import Flask, session, redirect, render_template, request, jsonify, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import psycopg2
import gc
import requests


app = Flask(__name__, static_url_path='/static')

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=6, max=10, message="Username must be between 4 and 10 characters")])
    email = TextField('Email Address', [validators.Length(min=10, max=20), validators.Required(message="This field cannot be empty")])
    password = PasswordField('New Password', [validators.Required(message="This field is Required"), validators.EqualTo('confirm', message='Passwords do not match'), 
    validators.Length(min=8, max=15, message="Password must be 8-15 characters long")])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated May, 2020)', [validators.Required()])



@app.route("/")
def index():
    return render_template("index.html")

@app.route('/register/', methods=["GET","POST"])
def register():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username  = request.form.get("username")
            email = request.form.get("email")
            password = sha256_crypt.encrypt((str(request.form.get("password"))))
            conn=psycopg2.connect("host=ec2-54-246-90-10.eu-west-1.compute.amazonaws.com dbname=d3lvkeb2pe1tju user=ojejhvdkytoheu password=e9fc09f3907c1fd2d9d9afc5b955e5ff392f42897c2f74b25c3bf4034fcc45d2")
            cur=conn.cursor()

            checkuser = cur.execute("""SELECT * FROM "users" WHERE username = username""",
                          {"username":request.form.get("username")})
            res = cur.fetchone()


            if res == 1:
                flash('That username is already taken, Please regoister again')
                return render_template('index.html', form=form)

            else:
                cur.execute("""INSERT INTO "users" VALUES (%(username)s, %(email)s, %(password)s)""",
                          {"username":request.form.get("username"), "email":request.form.get("email"),
                          "password":request.form.get("password")})
                
                conn.commit()
                flash("Thanks for registering!")
                cur.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return render_template('index.html')

        return render_template("register.html", form=form)

    except Exception as e:
        return(str(e))
		

