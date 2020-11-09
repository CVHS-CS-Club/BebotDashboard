from flask import Flask, render_template, session, redirect, request, url_for
import pymongo
from pymongo import MongoClient
import sys
import os
from oauth import Oauth

app = Flask(__name__)
app.secret_key = os.urandom(24)
cluster = pymongo.MongoClient("mongodb+srv://bebot:Yashveer1@bebot.qpm5l.mongodb.net/<dbname>?retryWrites=true&w=majority", maxPoolSize=50, connect=False)
db = cluster["Bebot"]
client = Oauth(app)


@app.route('/')
def index():
    count = db["MemberCount"].find({}).sort('$natural', pymongo.ASCENDING)
    guild_count = count[count.count() - 1]["guild_count"]
    member_count = count[count.count() - 1]["member_count"]
    print(guild_count, file=sys.stderr)
    return render_template('index.html', guild_count=guild_count, member_count=member_count)

@app.route('/features')
def features():
    return render_template('features.html')
@app.route('/dashboard')
def dashboard():
    try:
        code = request.args.get("code")
    except:
        if request.args.get('server') != None:
            return rendertemplate('dashboard.html')
        return redirect(url_for('.login'))
    try:
        session["token"] = client.get_access_token(code)["access_token"]
        session["user_data"] = client.get_user_json(session["token"])
        session["guilds_data"] = client.get_user_guilds(session["token"])
    except:
        return redirect(url_for('.login'))
    try:
        server = request.args.get('server')
        if server == None:
            raise Exception
    except:
        print("Redirecting to select server", file=sys.stderr)
        return redirect(url_for('.selectserver'))
    return render_template('dashboard.html')

@app.route('/selectserver')
def selectserver():
    try:
        userdata = session["user_data"]
        guilddata = session["guilds_data"]
    except:
        return redirect(url_for('.login'))
    servers = []
    for guild in guilddata:
        if guild["owner"]:
            print(guild['name'], file=sys.stderr)
            servers.append(guild)
    return render_template('login.html', servers=servers)
@app.route('/dashboardlogin')
def login():
    try:
        data = session["token"]
        return redirect(url_for('.dashboard?code=', _external=True))
    except:
        return redirect(client.getdiscorduri())

@app.route("/config/<state>")
def config(state):
    try:
        token = session["token"]
        user_data = session["user_data"]
        guild_data = session["guilds_data"]
    except:
        return redirect(url_for(".login", _external=True))
    if state == "welcomeon":
        return "Turning on welcome message"
    elif state == "welcomeoff":
        return "Turning off welcome message"
    else:
        return "Command uninplemented"
    
if __name__ == '__main__':
    app.run(debug=True) 