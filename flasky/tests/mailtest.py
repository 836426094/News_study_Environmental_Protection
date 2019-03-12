#coding=utf-8

from flask.ext.mail import Mail
from flask import Flask
from flask.ext.script import Manager
from flask_mail import Message
app=Flask(__name__)

mail=Mail(app)
manager=Manager(app)
# email server
MAIL_SERVER = 'c2.icoremail.net'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_DEBUG = app.debug
MAIL_USERNAME = 'qjt@ronhe.com'
MAIL_PASSWORD = '15278112919@bian'
MAIL_DEFAULT_SENDER = None
MAIL_MAX_EMAILS = None
# MAIL_SUPPRESS_SEND = app.testing
# MAIL_ASCII_ATTACHMENTS = False

# administrator list
ADMINS = ['836426094@qq.com']
@app.route("/")
def index():

    msg = Message("Hello",
                  sender="qjt@ronhe.com",
                  recipients=["836426094@qq.com"])

    # You can set the recipient emails immediately, or individually:
    # msg.recipients = ["you@example.com"]
    # msg.add_recipient("somebodyelse@example.com")
    # If you have set MAIL_DEFAULT_SENDER you don’t need to set the message sender explicity, as it will use this configuration value by default:
    # msg = Message("Hello",
    #               recipients=["to@example.com"])
    # If the sender is a two-element tuple, this will be split into name and address:
    # msg = Message("Hello",
    #               sender=("Me", "me@example.com"))
    # assert msg.sender == "Me <me@example.com>"
    # The message can contain a body and/or HTML:
    msg.body = "testing"
    msg.html = "<b>testing</b>"
    # Finally, to send the message, you use the Mail instance configured with your Flask application:

    mail.send(msg)
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

# if __name__=="__main__":
#     manager.run()