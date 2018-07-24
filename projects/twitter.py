# -*- encoding: utf-8 -*-
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

	def __init__(search_query, number, filename):
		self.query = search_query
		def num = number
		def fn = filename

	def setup_oauth():

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
	def get_oauth():


		oauth = OAuth1(CONSUMER_KEY,
					client_secret=CONSUMER_SECRET,
					resource_owner_key=OAUTH_TOKEN,
					resource_owner_secret=OAUTH_TOKEN_SECRET)
		return oauth

	def getMaxID(json):
		for x in range(0, len(json['statuses'])):
			if x == 0:
				min_id = json['statuses'][x]["id"]
			elif json['statuses'][x]["id"] < min_id:
				min_id = json['statuses'][x]["id"]

		return min_id

	def getLotOfTweets(search, number):
		result_type = "mixed"

		data = []
		tries = 1
		if number % 100 == 0:
			tries = int(round(number / 100))
			first_try = 100
		else:
			tries  = int(round(number / 100 + 1))
			first_try = number % 100

		for i in range(1, tries+1):
			if not OAUTH_TOKEN:
				token, secret = setup_oauth()
				print("OAUTH_TOKEN: " + token)
				print("OAUTH_TOKEN_SECRET: " + secret)
				print("______________________________")
			else:
				if i == 1:
					oauth = get_oauth()
					r = requests.get(url="https://api.twitter.com/1.1/search/tweets.json?q="+search+"&src=typd&count=" + str(first_try)+"", auth=oauth)
					data.append(r.json())
					max_id = getMaxID(data[i-1])
				else:
					oauth = get_oauth()
					r = requests.get(url="https://api.twitter.com/1.1/search/tweets.json?q="+search+"&src=typd&count=100&max_id="+str(max_id)+"&result_type="+result_type+"", auth=oauth)
					data.append(r.json())
					max_id = getMaxID(data[i-1])
		for x in range(1, len(data)):
			for y in range(0, len(data[x]["statuses"])):
				data[0]['statuses'].append(data[x]["statuses"][y])

		data = data[0]
		return data


	def twitter_rest (search, num, file_name):

		data = []
		print("Starting...")
		search = search.replace (" ", "%20")

		if not OAUTH_TOKEN:
			token, secret = setup_oauth()
			print("OAUTH_TOKEN: " + token)
			print("OAUTH_TOKEN_SECRET: " + secret)
			print("_______________________________")
		else:
			text = getLotOfTweets(search, num)
			data_file = open( 'projects/twitter/static/' + file_name +'.json', 'w')
			json.dump(text, data_file)
			data_file.close()
			for x in range(0,int(num)):
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

"""
def twitter_stream(seek, n, project, file="test.txt"):

	print("Starting stream...")

	
	seek = u""+seek+""


	class listener(StreamListener):

		def __init__(self):
			self.num = 0
		
		def on_data(self,data):
			try:
				
				if self.num <= n:
					self.num += 1
					global tweets
					text = json.loads(data)
					tex = text['text']
					saveFile = open('projects/twitter/' + file + '.csv', 'a')
					tweets = tweets + "||" + tex
					saveFile.write(tex)
					saveFile.write("\n")
					saveFile.close()
					print(self.num)
					#addtwits(text['id'], int(project), text['user']['id'], tex, text['user']['screen_name'])
					return True
				else:
					return False
			except BaseException as e:
				print("Failed: " + str(e))
				time.sleep(5)

	def on_error(status):
		print(status)

	auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
	twitterStream = Stream(auth, listener())
	twitterStream.filter(track=[seek])
	return tweets
"""





