#!/usr/bin/env python
import os
from FlaskWebProject import app
from flask import current_app, Flask, redirect, url_for, session
from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask import flash
from werkzeug.utils import secure_filename
from bson.binary import Binary
import gridfs
import base64
import datetime


def db_conn():
    client = MongoClient("mongodb://supriyadb:supriyadb@ds040489.mlab.com:40489/supriyadb")
    db = client.supriyadb
    collection = db.user
    return db


usern = None
grpn = None
# global username

print"connected"


@app.route('/', methods=['POST', 'GET'])
def run():
    return render_template('index.html')
    print "working"


@app.route('/newuser', methods=['POST', 'GET'])
def newuser():
    global usern
    db = db_conn()
    username = request.form['username']
    password = request.form['password']

    var = {
        'username': username,
        'password': password,
    }
    db.user.insert(var)
    output = """<h1> Sucessfully inserted, go back to login</h1>"""
    return output


@app.route('/login', methods=['POST', 'GET'])
def login():
    global usern
    global grpn
    db = db_conn()
    print "inside login"

    username = request.form['user']
    password = request.form['pass']
    count = db.user.find({'username': username, 'password': password}).count() > 0
    print count
    usern = username
    print(grpn)
    if count:
        text = "successfully logged in"
        return render_template("loginoutput.html", text=text)
    else:
        text = "please enter your username and password again"

        output1 = """<h1>%s</h1>""" % (text)
        return output1


@app.route('/uploadimage',methods=['POST', 'GET'])
def uploadimage():
    global usern
    db = db_conn()
    try:
        out = "Uploaded successfully"
        image_file = request.files['pic']
        prio = request.form['priority']
        #text_file=request.files['file']
        #print(text_file)
        #text=text_file.read()
        #print(text)
        print(image_file.filename)
        file_name = image_file.filename
        #text_file1=text_file.filename
        target = image_file.read()
        size=len(target)
        comm = request.form['comments']

        print(size)
        count = 0
        for item in db.fs.files.find({"user":usern}):
            print(item)
            count += 1
            print(count)
        if size<5000000:
            if count<100:
                # encoded_string=base64.b64encode(target)
                print ("inside if")
                fs = gridfs.GridFS(db)
                stored = fs.put(target, filename=file_name, user=usern, comment=comm,file_type="image",priority=prio)
                #stored1 = fs.put(text,filename=text_file1)
                print(stored)
            else:
                raise ValueError('count crossed')
        else:
            raise ValueError('size crossed')

    except:
        out = "upload failed"

    return render_template("insert.html", output=out)

@app.route('/uploadtext',methods=['POST', 'GET'])
def uploadtext():
    global usern
    db = db_conn()
    try:
        out = "successfully upload"
        text_file=request.files['file']
        print(text_file)
        text=text_file.read()
        print(text)
        file_name = text_file.filename
        print file_name
        #size=len(text)
        comm = request.form['comments']
        prio = request.form['priority']
        count = 0
        for item in db.fs.files.find({"user":usern}):
            print(item)
            count += 1
            print(count)
        if count<100:
            # encoded_string=base64.b64encode(target)
            print ("inside if")
            fs = gridfs.GridFS(db)
            stored = fs.put(text, filename=file_name, user=usern, comment=comm,file_type="text",priority=prio)
            #stored1 = fs.put(text,filename=text_file1)
            print(stored)
        else:
            raise ValueError('count crossed')

    except ValueError as e:
        out = e

    return render_template("insert.html", output=out)

@app.route('/fetchmine', methods=['POST', 'GET'])
def fetchmine():
    db = db_conn()
    fs = gridfs.GridFS(db)
    diclist = []
    global text

    for item in db.fs.files.find({"user":usern}):
        com = None
        file_name = item['filename']
        textfile_name=item['filename']
        file_type = item['file_type']
        priority = item['priority']
        print("getting text file name")
        print(textfile_name)
        if 'comment' in item.keys():
            com = item['comment']
        if 'uploadDate' in item.keys():
            date= item['uploadDate']
        if file_type == "image":
            picture = fs.find_one({"filename": file_name}).read()
            data = "data:image/jpeg;base64," + base64.b64encode(picture)
        if file_type == "text":
            data=fs.find_one({"filename": textfile_name}).read()

        dicvar = {}
        dicvar['file_type'] = file_type
        dicvar['file_name'] = file_name
        dicvar['com'] = com
        dicvar['image'] = data
        dicvar['priority']=priority
        dicvar['uploadDate']=date
        # print dicvar
        diclist.append(dicvar)
        # print diclist

    return render_template("display.html",lists=diclist)

@app.route('/fetch', methods=['POST', 'GET'])
def fetch():
    global usern
    db = db_conn()
    fs = gridfs.GridFS(db)

    diclist=[]


    for item in db.fs.files.find():
        com = None
        user_name = None
        file_name=item['filename']
        file_type=item['file_type']
        priority = item['priority']
        if 'user' in item.keys():
            user_name=item['user']
        if 'comment' in item.keys():
            com=item['comment']
        if 'uploadDate' in item.keys():
            date = item['uploadDate']
        if file_type=="image":
            picture=fs.find_one({"filename" : file_name }).read()
            data="data:image/jpeg;base64," + base64.b64encode(picture)

        if file_type=="text":
            data=fs.find_one({"filename" : file_name }).read()
        dicvar={}
        dicvar['file_type']=file_type
        dicvar['user']=user_name
        dicvar['file_name']=file_name
        dicvar['com']=com
        dicvar['image']=data
        dicvar['priority'] = priority
        dicvar['uploadDate'] = date


        diclist.append(dicvar)
        # print diclist

    return render_template("displayall.html", lists=diclist)


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    # if session.get('logged_in'):
    global usern
    db = db_conn()
    name = request.form['images']
    c = db.fs.files
    try:
        print("going inside try")
        c.delete_one({"filename": name})
        return redirect(url_for('fetchmine'))
    except:
        return "could not delete"
    # else:
    # return "u r not logged in"

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    # print("session is false")
    # session['logged_in'] = False
    # session.delete()
    return render_template("index.html")
