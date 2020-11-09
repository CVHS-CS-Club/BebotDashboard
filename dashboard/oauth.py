import requests
import sys
class Oauth(object):
    def __init__(self, app):
        self.app = app
        self.client_id = "769409130300440596"
        self.client_secret = "Gmdjs-6lkAtu-RCI_lVAJWz0KKCKKPh9"
        self.scope = "identify%20guilds"
        self.redirect_uri = "http://localhost:5000/dashboard"
        self.token_url = "https://discord.com/api/oauth2/token"
        self.base_uri = "https://discordapp.com/api"
    def getdiscorduri(self):
        discord_login_uri = f"https://discord.com/api/oauth2/authorize?client_id={self.client_id}&redirect_uri={self.redirect_uri}&response_type=code&scope={self.scope}"
        return discord_login_uri

    def get_access_token(self, code):
        payload = {
            "client_id": self.client_id,
            "client_secret":self.client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri":self.redirect_uri,
            "scope":self.scope}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        token = requests.post(self.token_url, headers=headers, data=payload).json()
        print(token, file=sys.stderr)
        return token
    
    def get_user_json(self, access_token):
        url = self.base_uri + "/users/@me"
        auth = f"Bearer {access_token}"
        print(auth, file=sys.stderr)
        headers = {
            "Authorization": auth
        }
        user_json = requests.get(url, headers=headers).json()
        return user_json

    def get_user_guilds(self, access_token):
        url = self.base_uri + "/users/@me/guilds"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        guilds = requests.get(url, headers=headers).json()
        return guilds