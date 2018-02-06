from __future__ import unicode_literals
import requests
from requests_oauthlib import OAuth1
from urllib import parse
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import time

auth = open("projects/twitter/auth.json", "r")
auth_json = json.load(auth)

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = auth_json['CONSUMER_KEY']
CONSUMER_SECRET = auth_json['CONSUMER_SECRET']
OAUTH_TOKEN = auth_json['OAUTH_TOKEN']
OAUTH_TOKEN_SECRET = auth_json['OAUTH_TOKEN_SECRET']

tweets = ""

class Twitter():



	def __init__(self, search_query, number, filename, result_type):
		self.query = search_query
		self.num = number
		self.fn = filename
		self.rt = result_type
		self.realn = 0

	def setup_oauth(self):

		"""Authorize your app via identifier."""
		# Request token
		oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
		r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
		credentials = parse(r.content)

		resource_owner_key = credentials.get('oauth_token')[0]
		resource_owner_secret = credentials.get('oauth_token_secret')[0]

		# Authorize
		authorize_url = AUTHORIZE_URL + resource_owner_key
		print('Please go here and authorize: ' + authorize_url)

		verifier = raw_input('Please input the verifier: ')
		oauth = OAuth1(CONSUMER_KEY,
					client_secret=CONSUMER_SECRET,
					resource_owner_key=resource_owner_key,
					resource_owner_secret=resource_owner_secret,
					verifier=verifier)

		# Finally, Obtain the Access Token
		r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
		credentials = parse(r.content)
		token = credentials.get('oauth_token')[0]
		secret = credentials.get('oauth_token_secret')[0]
		print(token)
		return token, secret

	def get_oauth(self):


		oauth = OAuth1(CONSUMER_KEY,
					client_secret=CONSUMER_SECRET,
					resource_owner_key=OAUTH_TOKEN,
					resource_owner_secret=OAUTH_TOKEN_SECRET)
		return oauth

	def getMaxID(self, json):
		for x in range(0, len(json['statuses'])):
			if x == 0:
				self.min_id = json['statuses'][x]["id"]
			elif json['statuses'][x]["id"] < self.min_id:
				self.min_id = json['statuses'][x]["id"]

		return self.min_id

	def getLotOfTweets(self):
		result_type = self.rt

		data = []
		tries = 1
		if self.num % 100 == 0:
			tries = int(round(self.num / 100))
			first_try = 100
		else:
			tries  = int(round(self.num / 100 + 1))
			first_try = self.num % 100

		for i in range(1, tries+1):
			if not OAUTH_TOKEN:
				token, secret = self.setup_oauth()
				print("OAUTH_TOKEN: " + token)
				print("OAUTH_TOKEN_SECRET: " + secret)
				print("______________________________")
			else:
				if i == 1:
					oauth = self.get_oauth()
					r = requests.get(url="https://api.twitter.com/1.1/search/tweets.json?q="+self.query+"&src=typd&count=" + str(first_try)+"", auth=oauth)
					data.append(r.json())
					max_id = self.getMaxID(data[i-1])
				else:
					oauth = self.get_oauth()
					r = requests.get(url="https://api.twitter.com/1.1/search/tweets.json?q="+self.query+"&src=typd&count=100&max_id="+str(max_id)+"&result_type="+result_type+"", auth=oauth)
					data.append(r.json())
					max_id = self.getMaxID(data[i-1])
		
		for x in range(1, len(data)):
			self.realn += len(data[x]["statuses"])
			print(self.realn)
			if len(data[x]["statuses"]) > 0:
				for y in range(0, len(data[x]["statuses"])):
					data[0]['statuses'].append(data[x]["statuses"][y])
			else:
				self.num = len(data[0]['statuses'])

		data = data[0]
		return data


	def rest (self):

		data = []
		print("Starting...")
		self.query = self.query.replace (" ", "%20")

		if not OAUTH_TOKEN:
			token, secret = setup_oauth()
			print("OAUTH_TOKEN: " + token)
			print("OAUTH_TOKEN_SECRET: " + secret)
			print("_______________________________")
		else:
			text = self.getLotOfTweets()
			data_file = open('projects/twitter/files/' + self.fn +'.json', 'w')
			json.dump(text, data_file)
			data_file.close()
			print("Recieved {0} of tweets".format(len(text['statuses'])))
			for x in range(0,int(self.realn)):
				try:
					tex = str(text['statuses'][x]['text']).encode('utf-8')
					texdat = text['statuses'][x]['created_at']
					texid = text['statuses'][x]['id_str']
					texid = int(texid.replace("u'", "").replace("'",""))
					uid = int(text['statuses'][x]['user']['id'])
					uscreen = text['statuses'][x]['user']['screen_name']
					uname = text['statuses'][x]['user']['name'].encode('utf-8')
					uloc = text['statuses'][x]['user']['location'].encode('utf-8')
					data.append([[tex], [texdat], [texid], [uscreen], [uname], [uloc], [uid],[uscreen]])
					record = open('research.txt', 'w')
					record.write(str(data))
					record.close()
				except Exception as e:
					print(e)
					data.append([['NO DATA'], ['-'], [123], ['USER NOT FOUND'], [e], ['Wasteland'], [21],['Courier']])


		return data

		def fulltime(self):

			r = requests.get()