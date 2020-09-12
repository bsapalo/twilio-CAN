from flask import Flask, render_template
from flask import request
import pyrebase
import urllib, os

from twilio.rest import Client

import send_data
app = Flask(__name__)

account_sid = "ACef20baf110bb81da947fa1f862f59e19"
auth_token = ""
client = Client(account_sid, auth_token)


@app.route('/')
def index():
    return render_template('91bee536-0b60-41b4-9199-583abb1480cf.html')

def get_image_url(filename):
    config = send_data.config
    firebase = pyrebase.initialize_app(config)

    storage = firebase.storage()
    files = storage.list_files()
    for file in files:
        image_url = storage.child(file.name).get_url(None)
    return image_url

numbers_dict = send_data.print_dict()
print(numbers_dict)

@app.route('/my-link/', methods=["POST"])
def my_link():
    if request.method == "POST":
        region = request.form["region"]
        text_message = request.form["text-message"]
        my_file = request.form["myfile"]
        image_url = get_image_url(my_file)
    for group in send_data.county_dict:
        if (region == group):
            print(group)
            temp_nums = []
            for county in send_data.county_dict[group]:
                print(county)
                for phone_num in numbers_dict[county]:
                    temp_nums.append(phone_num)
                    message = client.messages.create(from_='+19084482862', body= str(text_message), media_url=[image_url], to= str(phone_num))

            return "Your text has been sent!"
    return "Invalid County Given. Your text was NOT sent!"

if __name__ == '__main__':
  app.run(debug=True)
