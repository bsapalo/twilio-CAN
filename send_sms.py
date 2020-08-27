#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from twilio.rest import Client
from flask import Flask, request
import requests
import json

from twilio import twiml
from twilio.twiml.messaging_response import MessagingResponse
from pyngrok import ngrok
import time
import pyrebase



account_sid = "ACef20baf110bb81da947fa1f862f59e19"
auth_token = "75e82d30a92ac9d6ccb2458315ecb2f4"

client = Client(account_sid, auth_token)

report_names = {"1":"Alameda", "2":"Santa Clara", "3":"Contra Costa", "4":"San Francisco", "5":"San Mateo", "6":"Marin", "7":"Solano", "8":"Sonoma",
					"9":"Napa"}


config = {
    "apiKey": "AIzaSyDQBcsCLRd-yOPcMTAkGdp1zm3blzyT-g8",
    "authDomain": "bayareacan-35619.firebaseapp.com",
    "databaseURL": "https://bayareacan-35619.firebaseio.com/",
    "storageBucket": "bayareacan-35619.appspot.com",
    "serviceAccount": "./ServiceAccountKey.json"
}
firebase = pyrebase.initialize_app(config)

db = firebase.database()


app = Flask(__name__)

@app.route("/sms", methods=['GET','POST'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']
    if message_body in report_names.keys():
        with open("client.txt",'a') as file:
            file.write(number+'-->'+report_names[message_body]+'\n')
            file.close()
        data = {"phone_number": str(number), "county": report_names[message_body]}
        db.child("users").push(data)
        resp = MessagingResponse()
        resp.message("Thanks for joining BayAreaCan")
        return str(resp)
    else:
        message = client.messages \
            .create(
            from_='+19084482862',
            body="Text 1 if you live in  Alameda, 2 if you live in Santa Clara, 3 if you live in Contra Costa, 4 if you live in San Francisco, 5 if you live in San Mateo, 6 if you live in Marin, 7 if you live in Solano, 8 if you live in Sonoma, 9 if you live in Napa county",
            to= str(number)
        )
        return message.sid

if __name__ == '__main__':
    app.run()
