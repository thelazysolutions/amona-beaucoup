from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, get_flashed_messages, jsonify, Blueprint
from flask_cors import CORS, cross_origin
import os
from dotenv import load_dotenv
from flask import Flask,request,render_template
from flaskext.mysql import MySQL
import mysql.connector


conn = mysql.connector.connect(
   user="root", password="", host="127.0.0.1",  database="property_management" )


app = Flask(__name__)
app.secret_key = os.urandom(12)
cors = CORS(app)

from controllers.user import user
from controllers.client import client
from controllers.property import property
from controllers.image import image
from controllers.videos import video

from sqlalchemy import create_engine, MetaData, Table, Column, select, insert, and_, update
import inspect
from db.database import User,connection
from db.database import Client,connection
from db.database import Property,connection
from db.database import Images,connection
from db.database import Videos,connection


load_dotenv()


app.register_blueprint(property, url_prefix='/property/')
app.register_blueprint(user, url_prefix='/user/')
app.register_blueprint(client, url_prefix='/client/')
app.register_blueprint(image, url_prefix='/images/')
app.register_blueprint(video, url_prefix='/videos/')

@app.route('/',methods=['GET','POST'])
def view():
	return render_template('dashboard.html')


   
"""
@app.route('/user/',methods=['GET','POST'])
def addone():
    if request.method=='PUT':
        UserName=request.form.get['username']
        is_admin= request.form.get['usertype']
        email= request.form.get['useremail']
        passwd=request.form.get['userPass']
        conn = mysql.get_db()
        cursor = conn.cursor()
        query = "INSERT INTO `user` ( `name`, `is_admin`, `email`, `password`) VALUES (UserName,is_admin,email,passwd)"
        cursor.execute(query)
        conn.commit()
        conn.close()
    return 'Added successfully '




@app.route('/client/',methods=['GET','POST'])
def client():
    if request.method=='PUT':
        cli_name=request.form.get['clientname']
        cli_url= request.form.get['logo_url']
        cli_priority=request.form.get['priority']
        conn = mysql.get_db()
        cursor = conn.cursor()
        query = "INSERT INTO `client` ( `name`, `logo_url`, `priority`) VALUES (‘”. cli_name. “’,’”. cli_url .”’,’”. cli_priority .”’);"
        cursor.execute(query)
        conn.commit()
        conn.close()
        return 'Client Add success'
    return render_template('dashboard.html')


@app.route('/property/', methods=['GET','POST'])
def addOne():
    if request.method=='PUT':
        propertyName=request.form.get['prop_name']
        propertyDesc= request.form.get['prop_desc']
        propertyType=request.form.get['prop_Type']
        propertyLocat= request.form.get['prop_location']
        propertyPrice=request.form.get['prop_price']
        propertyDetails=request.form.get['prop_details']
        connection = mysql.get_db()
        cursor = connection.cursor()
        query = "INSERT INTO `property`( `name`, `description`, `type`, `location`, `price`, `details`) VALUES (propertyName,propertyDesc,propertyType,propertyLocat,propertyPrice,propertyDetails)"
        cursor.execute(query)
        connection.commit()
        return 'success'
    return render_template('dashboard.html')
    """
"""    
@app.after_request
def after_request(response):
    
    response.headers.add('Access-Control-Allow-Origin','*')
    #response.headers.add('Access-Control-Allow-Origin', '<origin>')
    #response.headers.add('Access-Control-Allow-Origin','*',origin,null)
    response.headers.add('Access-Control-Allow-Headers','Content-Type')
    return response 
"""    

if __name__ == "__main__":
    app.run(host=os.getenv('HOST'), port=os.getenv('PORT'), debug=True)