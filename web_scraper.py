# imports
from bs4 import BeautifulSoup
import requests
import urllib.request
import snscrape.modules.twitter as twitterScraper
from requests_html import HTMLSession
from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

#creates a new session
session = HTMLSession()

@app.route('/', methods=['POST', 'GET']) # post and get data
def index():
    if request.method == 'POST': 
        username = request.form["input-user"]
        if username == "":
            return render_template('index.html')
        else:
            return redirect(url_for("user", user=username))
    else:
        return render_template('index.html')
    
@app.route("/<user>", methods=['POST', 'GET'])
def user(user):
    if request.method == 'POST':
        username = request.form["input-user"]
        if username == "":
            return render_template('index.html')
        else:
            return render_template('index.html', user=username, instagram=instagram(username), reddit=reddit(username), pinterest=pinterest(username)
                            , youtube=youtube(username), twitter=twitter(username), snapchat=snapchat(username), spotify=spotify(username), github=github(username),
                            steam=steam(username, session), tumblr=tumblr(username), twitch=twitch(username, session), myspace=myspace(username), resultHeading="Results for '" + username + "'",
                            instagramUrl=instagramUrl(username), redditUrl=redditUrl(username), pinterestUrl=pinterestUrl(username), youtubeUrl=youtubeUrl(username), twitterUrl=twitterUrl(username), snapchatUrl=snapchatUrl(username),
                            spotifyUrl=spotifyUrl(username), githubUrl=githubUrl(username), steamUrl=steamUrl(username, session), tumblrUrl=tumblrUrl(username), twitchUrl=twitchUrl(username, session), myspaceUrl=myspaceUrl(username))
    else:
        return render_template('index.html', user=user, instagram=instagram(user), reddit=reddit(user), pinterest=pinterest(user)
                            , youtube=youtube(user), twitter=twitter(user), snapchat=snapchat(user), spotify=spotify(user), github=github(user),
                            steam=steam(user, session), tumblr=tumblr(user), twitch=twitch(user, session), myspace=myspace(user), resultHeading="Results for '" + user + "'",
                            instagramUrl=instagramUrl(user), redditUrl=redditUrl(user), pinterestUrl=pinterestUrl(user), youtubeUrl=youtubeUrl(user), twitterUrl=twitterUrl(user), snapchatUrl=snapchatUrl(user),
                            spotifyUrl=spotifyUrl(user), githubUrl=githubUrl(user), steamUrl=steamUrl(user, session), tumblrUrl=tumblrUrl(user), twitchUrl=twitchUrl(user, session), myspaceUrl=myspaceUrl(user))

# instagram
def instagram(user):
    # get results of the webpage from the url
    url = "https://www.instagram.com/" + user
    try:
        results = requests.get(url)
        doc = BeautifulSoup(results.text, "html.parser")

        # get the title from the HTML
        name = doc.title
    
    # first checks if there are too many request
    # then to see if the title exists
    # if the username matches in the title, return True
        if results.status_code == 429:
            return "yellow"
        elif user in name.string :
            return "green"
        else:
            return "red"
    except:
        return "red"

# reddit
def reddit(user):
    url = "https://www.reddit.com/r/" + user

    results = requests.get(url)
    doc = BeautifulSoup(results.text, "html.parser")

    # finds the h1 tag that contains the username
    name = doc.find(["h1"], string=user)

    try:
        if results.status_code == 429:
            return "yellow"
        elif name == None:
            return "red"
        elif user in name:
            return "green"
    except:
        return "red"
    
# pinterest
def pinterest(user):
    # puts input into lowercase
    username = user.lower()
    url = "https://www.pinterest.co.uk/" + username
    
    results = requests.get(url)
    doc = BeautifulSoup(results.text, "html.parser")
    
    # finds the exact HTML element with the specified class
    name = doc.find(class_="tBJ dyH iFc sAJ EdS zDA IZT swG")
    
    try:
        if results.status_code == 429:
            return "yellow"
        elif "@" + username in name.string :
            return "green"
        else:
            return "red"
    except:
        return "red"
    
# youtube
def youtube(user):
    url = "https://www.youtube.com/@" + user
    
    # Unfortunately, BeautifulSoup is not able to scrape Youtube.
    # Instead we will use urliib to check the status code of the web page
    # If the code returned is 200, the page exists and so does the username    
    try:
        status_code = urllib.request.urlopen(url).getcode()
        if status_code == 200:
            return "green"
    except urllib.error.HTTPError:
        return "red"

# twitter
def twitter(user):
    # Twitter is similar to youtube as BeautifulSoup struggles to scrape from twitter
    # Instead we will be using snscrape that can successfully get the username
    # This will search for the username and return if the "entity" exists
    try:
        scraper = twitterScraper.TwitterUserScraper(user)
        if scraper._get_entity():
            return "green"
        else:
            return "yellow"
    except ValueError:
        return "yellow"
    
# snapchat
def snapchat(user):
    url = "https://www.snapchat.com/add/" + user
    
    results = requests.get(url)
    doc = BeautifulSoup(results.text, "html.parser")
    
    # get the title from HTML
    name = doc.title
    
    try:
        if results.status_code == 429:
            return "yellow"
        elif user in name.string :
            return "green"
        else:
            return "red"
    except:
        return "red"
    
# spotify
def spotify(user):
    url = "https://open.spotify.com/user/" + user
    
    results = requests.get(url)
    doc = BeautifulSoup(results.text, "html.parser")
    
    name = doc.title
    
    try:
        if results.status_code == 429:
            return "yellow"
        elif user in name.string :
            return "green"
        else:
            return "red"
    except:
        return "red"

# github
def github(user):
    url = "https://github.com/" + user
    
    results = requests.get(url)
    doc = BeautifulSoup(results.text, "html.parser")
    
    name = doc.find(class_="p-nickname vcard-username d-block")
    
    try:
        if results.status_code == 429:
            return "yellow"
        elif user in name.string :
            return "green"
        else:
            return "red"
    except:
        return "red"

# steam
def steam(user, session):
    # Getting steam usernames is not easy since some URL's contain a numbered id
    # Also since the website is dynamic, we can't get data straight out of the HTML
    # Instead, we will use requests-html to run the HTML in the background then scrape the new HTML
    
    url = "https://steamcommunity.com/search/users/#text=" + user
    
    # rendering new HTML page
    r = session.get(url)
    r.html.render(sleep=1, keep_page=True, scrolldown=1)
    
    # find class name
    name = r.html.find('.searchPersonaName')
    
    # check if the username exists in the array that has been scraped
    try:
        if name[0]:
            return "green"
    except:
        return "red"
    
    
# tumblr
def tumblr(user):
    url = "https://www.tumblr.com/" + user
    
    results = requests.get(url)
    doc = BeautifulSoup(results.text, "html.parser")
    
    name = doc.find(class_="Da0mp")
    
    try:
        if results.status_code == 429:
            return "yellow"
        elif user in name:
            return "green"
    except:
        return "red"

# twitch
def twitch(user, session):
    url = "https://m.twitch.tv/search?term=" + user + "&type=channels"
    
    # rendering new HTML page
    r = session.get(url)
    r.html.render(sleep=1, keep_page=True, scrolldown=1)
    
    # find class name
    name = r.html.find('h4')
    
    username = []
    
    # iterate through all usernames on screen
    for title in name:
        # add to array
        username.append(title.text.lower())
    
    # If the username at the first position is == the username, then it exists
    # Only get the first position to save time and this is always the closest to the entered username
    try:
        if username[0] == user:
            return "green"
        else:
            return "red"
    except:
        return "red"
    
# myspace
def myspace(user):
    url = "https://myspace.com/" + user
    
    try:
        status_code = urllib.request.urlopen(url).getcode()
        if status_code == 200:
            return "green"
    except urllib.error.HTTPError:
        return "red"
    
def instagramUrl(user):
    if instagram(user):
        instagramUrl = "https://www.instagram.com/" + user
    return instagramUrl
    
def redditUrl(user):
    if reddit(user):
        redditUrl = "https://www.reddit.com/r/" + user
    return redditUrl

def pinterestUrl(user):
    if pinterest(user):
        pinterestUrl = "https://www.pinterest.co.uk/" + user
    return pinterestUrl

def youtubeUrl(user):
    if youtube(user):
        youtubeUrl = "https://www.youtube.com/@" + user
    return youtubeUrl

def twitterUrl(user):
    if twitter(user):
        twitterUrl = "https://twitter.com/" + user
    return twitterUrl

def snapchatUrl(user):
    if snapchat(user):
        snapchatUrl = "https://www.snapchat.com/add/" + user
    return snapchatUrl

def spotifyUrl(user):
    if spotify(user):
        spotifyUrl = "https://open.spotify.com/user/" + user
    return spotifyUrl

def githubUrl(user):
    if github(user):
        githubUrl = "https://github.com/" + user
    return githubUrl

def steamUrl(user, session):
    if steam(user, session):
        steamUrl = "https://steamcommunity.com/search/users/#text=" + user
    return steamUrl

def tumblrUrl(user):
    if tumblr(user):
        tumblrUrl = "https://www.tumblr.com/" + user
    return tumblrUrl

def twitchUrl(user, session):
    if twitch(user, session):
        twitchUrl = "https://m.twitch.tv/search?term=" + user + "&type=channels"
    return twitchUrl

def myspaceUrl(user):
    if myspace(user):
        myspaceUrl = "https://myspace.com/" + user
    return myspaceUrl
        
if __name__ == "__main__":
    app.run(threaded=False, host='0.0.0.0')