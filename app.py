from flask import Flask,render_template,request
from werkzeug.utils import secure_filename
import os
import csv
import pandas as pd
from func import main
from email.message import EmailMessage
import ssl
import smtplib
import zipfile
import io
import streamlit as st


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/',methods=['GET','POST'])
def hello_world():
    data = request.form
    n = request.form['singername']
    v = int(request.form['vdeos'])
    d = int(request.form['duration'])
    m = request.form['email']
    

    try:
        ans=main(n,v,d)
    except:
        return render_template('error.html')


    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as myzip:
        myzip.write("static/result.mp3", arcname="result.mp3")
    buffer.seek(0)

    with open("static/result.zip", "wb") as f:
        f.write(buffer.read())

    
    email_sender = "ngoel0209@gmail.com"
    email_password = "vstwcixvlrybzsnd"


    em = EmailMessage()
    em['From'] = email_sender
    em['Subject'] = 'Mail'
    with open("static/result.zip","rb") as fp:
        file_data=fp.read()
    em.add_attachment(file_data,maintype='application',subtype='zip',filename='result.zip')


    context = ssl.create_default_context()

    email_receiver = m
    em['To'] = email_receiver
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(em)

    os.remove("static/result.mp3")
    os.remove("static/result.zip")
    return render_template('form.html')
    

if __name__ == '__main__':
    app.run(debug=True,port=5001)