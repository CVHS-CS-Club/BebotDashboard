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

    
if __name__ == '__main__':
    app.run(debug=True) 