from flask import Flask, render_template, session
import pymongo
from pymongo import MongoClient
import sys
from requests_oauthlib import OAuth2Session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
client = pymongo.MongoClient("mongodb+srv://bebot:Yashveer1@bebot.qpm5l.mongodb.net/<dbname>?retryWrites=true&w=majority", maxPoolSize=50, connect=False)
db = client["Bebot"]


@app.route('/')
def index():
    count = db["MemberCount"].find({}).sort('$natural', pymongo.ASCENDING)
    guild_count = count[count.count() - 1]["guild_count"]
    member_count = count[count.count() - 1]["member_count"]
    print(guild_count, file=sys.stderr)
    return render_template('index.html', guild_count=guild_count, member_count=member_count)

@app.route('/dashboardlogin')
def login():
    client_id = r'769409130300440596'
    redirect_uri='https://localhost:5000'
    scope = ['identify', 'email']
    authorize_url = 'https://discordapp.com/api/oauth2/authorize'
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    login_url, state = oauth.authorization_url(authorize_url)
    session['state'] = state
    print("Login url: %s" % login_url)
    return render_template('dashboard.html', loginuri=login_url)
if __name__ == '__main__':
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem')) 
