from flask import Flask, render_template, session, redirect, request
import pymongo
from pymongo import MongoClient
import sys
from requests_oauthlib import OAuth2Session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
client = pymongo.MongoClient("mongodb+srv://bebot:Yashveer1@bebot.qpm5l.mongodb.net/<dbname>?retryWrites=true&w=majority", maxPoolSize=50, connect=False)
db = client["Bebot"]
token_url = 'https://discordapp.com/api/oauth2/token'
authorize_url = 'https://discordapp.com/api/oauth2/authorize'
client_id = r'769409130300440596'


@app.route('/')
def index():
    count = db["MemberCount"].find({}).sort('$natural', pymongo.ASCENDING)
    guild_count = count[count.count() - 1]["guild_count"]
    member_count = count[count.count() - 1]["member_count"]
    print(guild_count, file=sys.stderr)
    return render_template('index.html', guild_count=guild_count, member_count=member_count)

@app.route('/dashboard')
def dashboardbuffer():
    session["code"] = request.args.get("code")
    return render_template('login.html')

@app.route('/dashboardlogin')
def login():
    redirect_uri='https://localhost:5000/dashboard'
    scope = ['identify', 'email']
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    login_url, state = oauth.authorization_url(authorize_url)
    session['state'] = state
    print("Login url: %s" % login_url)
    return redirect(login_url, code=302)

@app.route("/config/<attribute>")
def config(attribute):
    try:
        code = session["code"]
    except:
        return redirect('https://localhost:5000/dashboardlogin')
    state = request.args.get("state")
    print(code, file=sys.stderr)
    if attribute == "welcome":
        if state == "off":
            return code
        elif state == "on":
            return code

if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc') 