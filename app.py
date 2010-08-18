#!/usr/bin/env python
# app.py
# Author: Andy Tibbs
# June 2, 2010

import os, urllib2, re, cgi
from time import strftime
import tweepy

# Google App Engine imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import memcache 

from models.models import OAuthToken
# Beautiful soup HTML parser
from build.BeautifulSoup import BeautifulStoneSoup


CONSUMER_KEY = 'YOUR CONSUMER KEY'
CONSUMER_SECRET = 'YOUR CONSUMER SECRET'
CALLBACK_URL = 'YOUR APP CALLBACK URL'
OAUTH = ''
CALLBACK = 0
KEY = ''
SECRET = ''
MAX_ACTIVITY = 20

class MainPage(webapp.RequestHandler):
 def get(self):
     self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
     user_agent = self.request.headers.get('User-Agent', '').lower()
     iphone = 'iphone' in user_agent or 'ipod' in user_agent
     values = 'NULL'
     os_path = os.path.dirname(__file__)
     oauth_token = self.request.get("oauth_token", None)
     if not CALLBACK:
        # Build a new oauth handler and display authorization url to user.
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, CALLBACK_URL)	 
        # status = memcache.get('auth_status')
        # memcache.set('auth_status', 'auth')
        try:
            auth_url = auth.get_authorization_url()
            request_token = auth.request_token
        except tweepy.TweepError:
            self.response.out.write('<p><span><b>Error! Failed to get the request token.</b></span></p>')
            return
        token = OAuthToken(token_key = auth.request_token.key, token_secret = auth.request_token.secret)
        token.put()
        self.redirect(auth_url)		 
     else:
       # token = OAuthToken.gql("WHERE token_key=:key", key=OAUTH).get()	 
       # auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, CALLBACK_URL)	
       # auth.set_access_token(KEY, SECRET)
       # api = tweepy.API(auth)

       if iphone:
           self.response.out.write(template.render(os.path.join(os_path, 'html/index_iphone.html'), None))
       else:
           path1 = os.path.join(os.path.dirname(__file__), 'html/index_p1.html')
           path2 = os.path.join(os.path.dirname(__file__), 'html/index_p2.html')
           self.response.out.write(template.render(os.path.join(path1), None))
           self.truck_Activity()
		   # while (count < 20):
				# self.response.out.write('<p><span><b>%s: </b></span>' %names[count])
				# self.response.out.write('"%s" ' %tweets[count])
				# self.response.out.write(' -- %s</p>\n' %times[count])
				# count += 1
       self.response.out.write(template.render(os.path.join(path2), None))

 def truck_Activity(self):
     tweets, names, times = [], [], [] 
     auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, CALLBACK_URL)	
     auth.set_access_token(KEY, SECRET)
     api = tweepy.API(auth)
     trucks = api.list_timeline('mrtibbs309','grubb')
     for t in trucks:
	     # Grab tweets
         tweets.append(t.text)
	     # Grab truck names
         names.append(t.user.name)
	     # Grab time of tweet (Need to add additional timezone support)
         time = t.created_at
         time = time.strftime('%I:%M')
         time_hr = (int(time[0:2]) + 5 ) % 12
         if not time_hr:
           time_hr = 12
         time_hr = str(time_hr)
         time = time_hr + time[2:]
         # self.response.out.write(' -- %s </p>\n' % time)
         times.append(time)		 
     self.display_Top(tweets, names, times)
		 
 def display_Top(self, tweets, names, times):
     cnt = 0
     while (cnt < MAX_ACTIVITY):
         self.response.out.write('<p><span><b>%s: </b></span>' % names[cnt])
         self.response.out.write('"%s" ' % tweets[cnt])
         self.response.out.write(' -- at %s</p>\n' % times[cnt])
         cnt += 1	 
	 
def set_CALLBACK():
    global CALLBACK    # Needed to modify global copy of CALLBACK
    CALLBACK = 1
	
# Callback page (/oauth/callback)
class Callback(webapp.RequestHandler):
    def get(self):
        global KEY
        global SECRET
        global OAUTH
        oauth_token = self.request.get("oauth_token", None)
        oauth_verifier = self.request.get("oauth_verifier", None)
        # Invalid request check
        if oauth_token is None:
            self.response.out.write('<p><span><b>OAuth token request fail.</b></span></p>')
            return				
		# Lookup the request token
        token = OAuthToken.gql("WHERE token_key=:key", key=oauth_token).get()
        if token is None:
            self.response.out.write('<p><span><b>Unable to retrieve token. </b></span></p>')
            return
		# Rebuild the OAuth handler
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, CALLBACK_URL)				
        auth.set_request_token(token.token_key, token.token_secret)	
		# Fetch the access token
        try:
            auth.get_access_token(oauth_verifier)
            api = tweepy.API(auth)
            # token = request_token.request_token
            twitterName = api.me().screen_name
        except tweepy.TweepError:
            self.response.out.write('<p><span><b>Error! Failed to get the access token. </b></span></p>')
		# Store access key for rebuilding elsewhere				
        token.access_token_key = auth.access_token.key
        token.access_token_secret = auth.access_token.secret
        token.verifier = oauth_verifier		
        token.put()
        KEY = auth.access_token.key
        SECRET =  auth.access_token.secret
        OAUTH = oauth_token
		# memcache.set('access_token_key', auth.access_token.key)
        # memcache.set('access_token_secret', auth.access_token.secret)	
        # memcache.set('token_verifier', oauth_verifier)

        # trucks = api.list_timeline('mrtibbs309','grubb')
        # self.response.out.write('%s' %times)		
        # self.response.out.write('<p><span><b>Congrats! You are connected as %s </b><span></p>' % twitterName)
        # self.response.out.write('<p><span><b> %s </b></span></p>' % times)
        set_CALLBACK()
        self.redirect('/')
		 
application = webapp.WSGIApplication([
  (r'/oauth/callback', Callback),
  (r'/.*$', MainPage),
], debug=True)

def main():
 run_wsgi_app(application)

if __name__ == "__main__":

 main()
