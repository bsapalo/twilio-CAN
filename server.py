from flask import Flask, render_template
from flask import request
import pyrebase

from twilio.rest import Client

import send_data
app = Flask(__name__)

account_sid = "ACef20baf110bb81da947fa1f862f59e19"
auth_token = "3cf6b9bdde2574221847b5027d59d483"
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

  #   const images = firebase.storage().ref().child('companyImages');
  # const image = images.child('image1');
  # image.getDownloadURL().then((url) => { this.setState({ img: url }));

@app.route('/my-link/', methods=["POST"])
def my_link():
    if request.method == "POST":
        region = request.form["region"]
        text_message = request.form["text-message"]
        my_file = request.form["myfile"]
        image_url = get_image_url(my_file)
    numbers_dict = send_data.print_dict()
    for group in send_data.county_dict:
        if (region == group):
            print(group)
            for county in send_data.county_dict[group]:
                print(county)
                for phone_num in numbers_dict[county]:
                    message = client.messages.create(from_='+19084482862', body= str(text_message), media_url=[image_url], to= str(phone_num))

            return "Your text has been sent!"
    return "Invalid County Given. Your text was NOT sent!"

if __name__ == '__main__':
  app.run(debug=True)
