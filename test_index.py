
import pytest
import flask
from flask import Flask

def test_db():

    try:
        conn = psycopg2.connect("host=ec2-46-137-156-205.eu-west-1.compute.amazonaws.com dbname=d2mq7ob78bs26e user=icatkfqgctigtb password=da2cf2266c7a1cb169ef6f4b3db782c4822805680db0e1fe86a626bd4d5dbab5 connect_timeout=1")
        conn.close()
        return True
    except:
        return False



def test_ind():
	app = flask.Flask(__name__)
	client = app.test_client()

	res = client.get('/index.html')
	#assert res.status_code == 200


