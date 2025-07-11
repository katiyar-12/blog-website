from flask import Flask , render_template , request
import requests
import smtplib
import os

from dotenv import load_dotenv , dotenv_values
load_dotenv()


app = Flask(__name__)

blog_url = os.getenv('blog_url')
response = requests.get(url=blog_url)

def get_id(post_id) :
    for blog in response.json() :
        if blog["id"] == post_id :
            return blog
    return None


@app.route("/")
def home():
    data = response.json()
    return render_template("index.html",data=data)


@app.route("/contact")
def contact() :
    return render_template("contact.html")

@app.route("/post/<int:post_id>")
def post(post_id) :
    blog = get_id(post_id)
    return  render_template("post.html",blog=blog)

@app.route("/contact/send",methods=["POST" , "GET"])
def send() :
    name = request.form.get("sender_name")
    email = request.form.get("sender_email")
    mobile = request.form.get("sender_mobile")
    message_ = request.form.get("message")

    my_email_sender = os.getenv('my_email_sender')
    my_email_receiver = os.getenv('my_email_receiver')


    client = smtplib.SMTP("smtp.gmail.com",587)
    client.starttls()
    client.login(my_email_sender ,os.getenv('blog_website_app_password') )

    message = f"Subject : You Have a message from {name}\n\nSenders Email : {email}\n\nMobile No : {mobile}\n\n\nMessage : {message_} "
    client.sendmail(my_email_sender ,my_email_receiver ,message)
    client.quit()

    return render_template('success.html')


@app.route("/about")
def about() :
    return render_template("about.html")

if __name__ == "__main__" :
    app.run(debug=True)
