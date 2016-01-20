'''from urllib.request import urlopen
import os
import json

if not os.path.exists('../../images/emotes'):
    os.makedirs('../../images/emotes')
print('Saving emotes to folder: ' + os.path.abspath('./emotes') + '...')
print('Grabbing emote list...')
emotes = json.load(urlopen('https://twitchemotes.com/api_cache/v2/global.json'))
for code, emote in emotes['emotes'].items():
    print('Downloading: ' + code + '...')
    urllib.urlretrieve('http:' + emotes['template']['large'].replace('{image_id}', str(emote['image_id'])),
                       './emotes/' + code + '.png')
print('Done! Kappa')'''

from urllib.request import urlopen
import urllib
import os
import json

if not os.path.exists('./emotes'):
    os.makedirs('./emotes')
print('Saving emotes to folder: ' + os.path.abspath('./emotes') + '...')
print('Grabbing emote list...')
response = urlopen('https://twitchemotes.com/api_cache/v2/global.json')
response = urllib.parse.rlencode(response)
emotes = json.load(response)
for code, emote in emotes['emotes'].items():
    print('Downloading: ' + code + '...')
    urllib.urlretrieve('http:' + emotes['template']['large'].replace('{image_id}', str(emote['image_id'])),
                       './emotes/' + code + '.png')
print('Done! Kappa')