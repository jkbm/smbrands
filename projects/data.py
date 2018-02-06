# -*- encoding: utf-8 -*-
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import time
#from db import addtwits

auth = open("projects/twitter/auth.json", "r")
auth_json = json.load(auth)

ckey = auth_json['CONSUMER_KEY']
csecret = auth_json['CONSUMER_SECRET']
atoken = auth_json['OAUTH_TOKEN']
asecret = auth_json['OAUTH_TOKEN_SECRET']


tweets = ""






def data_stream(seek, n, project, file="test.txt"):

	print("Starting stream...")
 

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
					print(tex)
					#addtwits(text['id'], int(project), text['user']['id'], tex, text['user']['screen_name'])
					return True
				else:
					return False
			except BaseException as e:
				print("Failed: " + str(e))
				time.sleep(5)

	def on_error(status):
		print(status)

	auth = OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken, asecret)
	twitterStream = Stream(auth, listener())
	twitterStream.filter(track=[seek])
	return tweets