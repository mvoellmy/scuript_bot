import urllib
import requests
import os
import json

if not os.path.exists('./emotes'):
    os.makedirs('./emotes')

print('Saving emotes to folder: ' + os.path.abspath('../../emotes') + '...')
print('Grabbing emote list...')

# Why does this not work?
emotes_res = requests.get('https://twitchemotes.com/api_cache/v2/global.json')

print(emotes_res.status_code)

emotes = emotes_res.json()

for code, emote in emotes['emotes'].items():
    print('Downloading: ' + code + '...')
    urllib.request.urlretrieve('http:' + emotes['template']['large'].replace('{image_id}', str(emote['image_id'])),
                      './emotes/' + code + '.png')

print('Done! Kappa')