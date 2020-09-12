#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import pyrebase
from collections import defaultdict
import cgi


county_dict = {"1" : ["Alameda", "Contra Costa"], "2" : ["Santa Clara"], "3": ["San Mateo", "San Francisco"],
               "4": ["Marin", "Sonoma"], "5":["Solona","Napa "]}

writers_dict = {"Alameda":"Kevin", "Contra Costa":"Jaida", "Santa Clara":"Pranav", "San Mateo":"Trenton", "San Francisco":"Henry",
                "Marin":"Arthur","Sonoma":"Kayla","Solona":"Anika","Napa":"Khanh"}

final_dict = {}

for key in county_dict.items():
    for county in key[1]:
        final_dict[county] = []

config = {
    "apiKey": "AIzaSyDQBcsCLRd-yOPcMTAkGdp1zm3blzyT-g8",
    "authDomain": "bayareacan-35619.firebaseapp.com",
    "databaseURL": "https://bayareacan-35619.firebaseio.com/",
    "storageBucket": "bayareacan-35619.appspot.com",
    "serviceAccount": "./ServiceAccountKey.json"
}
firebase = pyrebase.initialize_app(config)

def print_dict():
    db = firebase.database()

    all_users = db.child("users").get()
    for user in all_users.each():
        data = user.val()
        try:
            final_dict[data['county']].append(data["phone_number"])
        except KeyError:
            pass

    return final_dict
