import urllib
import requests
import os
import json

if not os.path.exists('./emotes'):
    os.makedirs('./emotes')
print('Saving emotes to folder: ' + os.path.abspath('./emotes') + '...')
print('Grabbing emote list...')

# Why does this not work?
response = requests.get('https://twitchemotes.com/api_cache/v2/global.json')
response.status_code

#emotes = json.load(urllib.urlopen('https://twitchemotes.com/api_cache/v2/global.json'))
#for code, emote in emotes['emotes'].items():
#    print('Downloading: ' + code + '...')
#    urllib.urlretrieve('http:' + emotes['template']['large'].replace('{image_id}', str(emote['image_id'])),
#                       './emotes/' + code + '.png')

print('Done! Kappa')