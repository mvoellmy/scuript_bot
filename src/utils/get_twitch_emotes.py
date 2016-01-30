import urllib
import requests
import os
import json

EMOTES_PATH = '../images/emotes/'


def get_emotes():
	if not os.path.exists(EMOTES_PATH):
	    os.makedirs(EMOTES_PATH)

	print('Saving emotes to folder: ' + os.path.abspath(EMOTES_PATH) + '...')
	print('Grabbing emote list...')

	# Why does this not work?
	emotes_res = requests.get('https://twitchemotes.com/api_cache/v2/global.json')

	print(emotes_res.status_code)

	emotes = emotes_res.json()

	for code, emote in emotes['emotes'].items():
	    print('Downloading: ' + code + '...')
	    urllib.request.urlretrieve('http:' + emotes['template']['large'].replace('{image_id}', str(emote['image_id'])),
	                      EMOTES_PATH + code + '.png')

	print('Done! Kappa')
	return True