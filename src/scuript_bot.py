#imports
import sys
sys.path.append('utils/')

import logging, logging.config
import discord
import getpass
import configparser
import copy
import time
import zxlolbot
import os
import os.path
import random

from collections import deque
from decimal import Decimal

# Scuript Modules
from league_utils import get_match_details
from league_utils import get_region_params
from league_utils import get_regions
from get_twitch_emotes import get_emotes
from get_twitch_emotes import EMOTES_PATH

## SCURIPT BOT ##
logging.config.fileConfig('../cfg/logging.conf')
logger = logging.getLogger("scuript_logger.bot")

# Read cfg.txt
config = configparser.ConfigParser()   
config.read('../cfg/cfg.txt')
username_discord = config.get('scuriptdiscord', 'username_discord')
password_discord = config.get('scuriptdiscord', 'password_discord')
username_lol = config.get('scuriptlol', 'username_lol')
password_lol = config.get('scuriptlol', 'password_lol')

# milleniumfalcon
client = discord.Client()
server_id = '114100951719215113'

_join = True

# generate emotes list
emotes_list = []
emotes_list = [f for f in os.listdir(EMOTES_PATH) if os.path.isfile(os.path.join(EMOTES_PATH, f))]
emotes_list = [emote.replace('.png', '') for emote in emotes_list]


#########################################################################################
# TODO add all discord related code to the scuriptdiscord class
# Commands for the bot
@client.event
def on_message(message):
    placeholder = "\n \t"
    commands =  {"!tutorial"                 : "Guide to setup your sound in Discord",
                "!currgame <SUMMONER_NAME>"  : "Check if your buddy is playing League of Legends and spectate him!\n \tOptions: -<REGION>",
                "!search <SEARCH_TERM>"      : "Searches channel history.\n \tOptions: -any, -here",
                "!callouts <MAP_NAME>"       : "Don't know where 'Tunnels' or 'A-long' is? Enter the CS:GO map name to learn.",                 
                "!join <SERVER_URL>"         : "enter your (SERVER_URL)",
                "!cleanup <OPTIONS>"         : "Delete the chatlog. \n \tOptions: -all, -bot, -cmds, -self",
                "!help more"                 : "more stuff"}

    more_commands =  {
                "!version"                   : "Look up the current version of scuript_bot!.",
                "!rekt"                      : "get r3kt m8", 
                "!hello"                     : "Say 'Hello' to scuript_bot!", 
                "!git"                       : "Link to the github repo.", 
                "!tts <YOUR_TEXT>"           : "Let the bot speak for you!",
                "!set_game <GAME_NAME>"      : "Set the game of SCURIPT_BOT (Admin only).",
                "!emotes"                    : "Get available emotes."}

    if message.content == '!get_emotes' and is_admin(message.author):
        client.send_typing(message.channel)
        if get_emotes():
            client.send_message(message.channel, 'All emotes have been downloaded. Restart Bot to use them.')
        else:
            client.send_message(message.channel, 'There has been an error with downloading the emotes.')

   
    elif message.content == '!emotes':
        emote_msg = 'All available emotes:\n'
        for emote in emotes_list:
            emote_msg = emote_msg + str(emote) + '\n'
        client.send_message(message.author, emote_msg)
        client.send_message(message.channel, 'A list with the available emotes has been sent to {0}.'.format(message.author.mention()))

    elif message.content == '!sclol':
        logger.debug('I am in !sclol')
        print('I will try to send this to summoner: @fox3ye') 
        #todo send this message to summoner....


    elif message.content == '!help':
        logger.debug('I am in !help')
        help_msg = "Looks like somebody needs help, lets see what we can do for you! beep-boop:\n \n"
        for k,v in commands.items():
            help_msg+='`{0}`{1}{2}\n'.format(k, placeholder, v)

        client.send_message(message.channel, help_msg)

    elif message.content == '!help more':
        logger.debug('I am in !help more')
        help_msg = "Here are some more commands:\n \n"
        for k,v in more_commands.items():
            help_msg+='`{0}`{1}{2}\n'.format(k, placeholder, v)

        client.send_message(message.channel, help_msg)

    elif message.content == '!hello':
        logger.debug('I am in !hello')
        client.send_message(message.channel, 'Hello received. Thank you! beep-boop')


    elif message.content == '!version':
        logger.debug('I am in !version')        
        client.send_message(message.channel, 'SCURIPT BOT VERSION 0.0.4!')
 
    elif message.content == '!tutorial':
        logger.debug('I am in !tutorial')
        tutorial(message.channel)

    elif message.content.startswith('!join'):
        logger.debug('I am in !join')
        url = message.content.replace("!join ", "")
        client.accept_invite(url)
        client.send_message(message.channel, "SCURIPT_BOT successfully joined your channel!")

    elif message.content.startswith('!set_game') and is_admin(message.author):
        logger.debug('I am in !set_game')
        scuript_bot_game = game('with your feelings...') 
        game_name = str(message.content.replace('!set_game ',''))
        scuript_bot_game.set_name(game_name)
        client.change_status(scuript_bot_game)
        #client.send_message(message.channel, 'The bot game has been successfully changed to {0}.'.format(game.name))

    elif message.content == '!git':
        logger.debug('I am in !git')
        client.send_message(message.channel, 'https://github.com/mvoellmy/scuript_bot')

    elif message.content.startswith('!tts'):
        logger.debug('I am in !tts')
        tts_msg = message.content.replace("!tts ", "")
        tts_msg = 'Beep, boop. ' + tts_msg + '. Beep, boop.'
        client.send_message(message.channel, tts_msg, True, True)

    elif message.content.startswith('!rekt'):
        logger.debug('I am in !rekt')

        rekt_list = ['You got rekt, son!',
                     'Lol. Rekt!',
                     'Damn son. Get rekt!',
                     'U wot mate?',
                     'You sir just experienced a wreckoning!',
                     'REKT! REKT! REKT!',
                     'Get noscoped bitch!',
                     'Mom get the camera! This guy got rekt!',
                     'rekekekekekekekeket!',
                     'hue hue hue hue. Morde es numero uno.',
                     'Get rekt, son!',
                     'Rekt!',
                     'Get rekt, biatch!',
                     'R-E-K-T']

        tts_msg = random.choice(rekt_list)

        client.send_message(message.channel, tts_msg, True, True)

        img_num = str(random.randint(1,150))
        rekt_path = ('../images/rekt/rekt_img_num_placeholder.jpg')
        rekt_path = rekt_path.replace('img_num_placeholder', img_num)

        if os.path.isfile(rekt_path):
            rekt_img = open(rekt_path,"rb")
            client.send_file(message.channel, rekt_img)
        else:
            client.send_message(message.channel, "No image was found with the name 'rekt_{0}.jpg'".format(img_num))

    elif message.content.startswith('!currgame'):
        logger.debug('I am in !currgame')
        client.send_typing(message.channel)
        
        summoner_name = message.content.replace('!currgame ', "")

        region_name = 'EUW'
        regions = get_regions()

        for region in regions:
            temp_region = '-' + region
            if temp_region.lower() in message.content.lower():
                region_name = region
                summoner_name = summoner_name.replace(temp_region.lower(), '')
                summoner_name = summoner_name.replace(temp_region.upper(), '')
                break

        region_params = get_region_params(region_name)

        match_details = get_match_details(summoner_name, region_name)

        show_champion_details = False
        if not match_details:
            game_details = "`Summoner '{0}' is currently not in a game..`".format(summoner_name)

        elif match_details.get('queue_type') == 'unknown' and match_details.get('game_length') == 'unknown':
           game_details = "`Are you sure summoner: '{0}', is currently ingame?`".format(summoner_name)   

        elif match_details.get('queue_type') == 'unknown':
            show_champion_details = True
            client.send_message(message.channel, match_details.get('champion_image'))
            game_details = "`Summoner '{0}' appears to be ingame as {1} {2} on {5} for {3} minutes. But unfortunately the game mode is: {4} :(.`".format(summoner_name, match_details.get('champion_name'), match_details.get('champion_title'), match_details.get('game_length'), match_details.get('queue_type'), region_params['Region'])
        
        else:
            show_champion_details = True
            client.send_message(message.channel, match_details.get('champion_image'))
            game_details = "`Summoner '{0}' is currently playing {1} {2}: {3} on {5} for {4} minutes.`".format(summoner_name, match_details.get('champion_name'), match_details.get('champion_title'), match_details.get('queue_type'), match_details.get('game_length'), region_params['Region'])
            

        client.send_message(message.channel, game_details)

        if show_champion_details:            

            client.send_message(message.channel, "`\n \t Ranked stats with: {0}\n \t won: {1}\n \t lost: {2}\n \t ratio: {3}`".format(match_details.get('champion_name'), match_details.get('games_won'), match_details.get('games_lost'), match_details.get('win_ratio')))

            # Specatate Mode encryption key
            spectate_file_stream = open('../bat/op_gg_spectate_template.bat','r')
            spectate_file_content = spectate_file_stream.read()
            spectate_file_stream.close()
            # Add correct encryption_key and game_id to bat file
            spectate_file_content = spectate_file_content.replace("encryptionKeyPlaceholder", match_details.get('encryption_key'))           
            spectate_file_content = spectate_file_content.replace("gameIdPlaceholder", str(match_details.get('game_id')))           
            spectate_file_content = spectate_file_content.replace("platformIdPlaceholder", str(region_params['PlatformID']))           
            spectate_file_content = spectate_file_content.replace("domainPlaceholder", str(region_params['Domain']))           
            spectate_file_content = spectate_file_content.replace("portPlaceholder", str(region_params['Port']))           

            spectate_file_stream = open('../bat/op_gg_spectate_customized.bat','w')
            spectate_file_stream.write(spectate_file_content)
            spectate_file_stream.close()
            
            op_gg_bat = open('../bat/op_gg_spectate_customized.bat',"rb")
            client.send_message(message.channel, 'Spectate the game by downloading and opening the following file:')          
            client.send_file(message.channel, op_gg_bat)
            # client.send_message(message.channel, 'Yes, Windows thinks its unsafe. \nNo, it is no virus. ;)')          



    elif message.content.startswith('!search') and str(message.author).lower() != 'SCURIPT_BOT'.lower():
        logger.debug('I am in !search')

        number_of_requests = 10;
        result_count = 0
        search_count = 0
        search_list = []
        results = []
        single_message_array = []

        _any = False

        search_msg = message.content.replace('!search ', "")
        search_list = search_msg.split()
        before_msg = message

        destination = message.author

        if '-here' in search_list:
            destination = message.channel
            search_list.remove('-here')

        if '-any' in search_list:
            _any = True
            search_list.remove('-any')

        client.send_typing(message.channel)
        for request in range(0, number_of_requests):
            search_messages = client.logs_from(message.channel, 100, before_msg)
            for it_msg in search_messages:
                search_count = search_count + 1
                if all(x.lower() in str(it_msg.content).lower() for x in search_list) and str(it_msg.author).lower() != 'SCURIPT_BOT'.lower() and it_msg.content.startswith('!') is not True:
                    results.append(it_msg)
                    result_count = result_count + 1

                elif _any and any(x.lower() in str(it_msg.content).lower() for x in search_list) and str(it_msg.author).lower() != 'SCURIPT_BOT'.lower() and it_msg.content.startswith('!') is not True:
                    results.append(it_msg)
                    result_count = result_count + 1

            before_msg = it_msg


        # Print Results
        if result_count > 1:
            single_message_array = stitch_messages(results)
            single_message_array.append('---------------------------------------\n{1} matching results have been found in the {0} channel of the {3}! ({1}/{2})'.format(message.channel.name, result_count, search_count, message.channel.server.name))
        elif result_count == 1:
            single_message_array = stitch_messages(results)
            single_message_array.append('---------------------------------------\n{1} matching result has been found in the {0} channel of the {3}! ({1}/{2})'.format(message.channel.name, result_count, search_count, message.channel.server.name))
        else:
            single_message_array.append('---------------------------------------\nNo matching result have been found in the {0} channel of the {3}! ({1}/{2}\nTry !help <search_text> -any to search if any words of your search can be found.)'.format(message.channel.name, result_count, search_count, message.channel.server.name))

        for single_message in single_message_array:
            client.send_message(destination, single_message)

        if destination == message.author:
            client.send_message(message.channel, '{0} I sent you a message with the results of your search.'.format(message.author.mention()))




    elif message.content.startswith('!mbr_join') and is_admin(message.author):
        logger.debug('I am in !mbr_join')
        search_msg = message.content.replace('!mbr_join ', "")
        if search_msg == 0:
            member_join = False
            client.send_message(message.channel,"Turned welcome messages off.")
        elif search_msg == 1:
            member_join = True
            client.send_message(message.channel,"Turned welcome messages on.")
        else:
            client.send_message(message.channel,"Unvalid mbr_join argument.")

    elif message.content.startswith('!callouts'):
        logger.debug('I am in !callouts')
        message.content = message.content.replace('!callouts ', "")
        message.content = message.content.replace('de_',"")
        message.content = message.content.replace('ar_',"")
        message.content = message.content.replace('cs_',"")

        callouts_path = ('../images/callouts/map_name_placeholder.jpg')
        callouts_path = callouts_path.replace('map_name_placeholder', message.content)
        
        if os.path.isfile(callouts_path):
            callouts_map = open(callouts_path,"rb")
            client.send_message(message.channel, "`Callouts for {0}:`".format(message.content))
            client.send_file(message.channel, callouts_map)
        else:
            client.send_message(message.channel, "No callouts-map was found for '{0}.'".format(message.content))

    elif message.content.startswith('!cleanup') and is_admin(message.author):
        logger.debug('I am in !cleanup')

        _bot = False
        _cmds = False
        _self = False
        _all = False 

        number_of_requests = 1

        if '-bot' in message.content:
            _bot = True
        
        if '-cmds' in message.content:
            _cmds = True
        
        if '-self' in message.content:
            _self = True

        if '-all' in message.content:
            _all = True

        result_count = 0
        search_count = 0
        before_msg = message

        client.send_typing(message.channel)

        for request in range(0, number_of_requests):
            search_messages = client.logs_from(message.channel, 100, before_msg)
            for it_msg in search_messages:
                search_count = search_count + 1
                if _bot and str(it_msg.author).lower() == 'SCURIPT_BOT'.lower():
                    client.delete_message(it_msg)
                    result_count = result_count + 1
                elif _cmds and it_msg.content.startswith('!'):
                    client.delete_message(it_msg)
                    result_count = result_count + 1    
                elif _self and str(it_msg.author).lower() == str(message.author.lower()):
                    client.delete_message(it_msg)
                    result_count = result_count + 1
                elif _all:
                    client.delete_message(it_msg)
                    result_count = result_count + 1
            before_msg = it_msg

        client.send_message(message.channel,"{0} matching results have been deleted! ({0}/{1})".format(result_count, search_count))

    for emote in emotes_list:
        if emote in message.content and str(message.author).lower() != 'SCURIPT_BOT'.lower():
            logger.debug('I am in !emotes')
            emote_path = EMOTES_PATH + emote + '.png'
            emote_img = open(emote_path,"rb")
            client.send_file(message.channel, emote_img)


# Event for joining members
@client.event
def on_member_join(member):
    if member_join == True:
        server = member.server
        client.send_message(server, 'Welcome {0} to the glorious {1.name} server!'.format(member.mention(), server))
        tutorial(member)
        client.send_message(server, '{0} I sent you a message with instructions on how to setup your sound!'.format(member.mention()))

# Commandline output on startup
@client.event
def on_ready():
    logger.debug('Logged in as')
    logger.debug(client.user.name)
    logger.debug('ID:')
    logger.debug(client.user.id)
    logger.debug('------')

    # Set Default Game of Scuript Bot
    scuript_bot_game = game('with your feelings...') 
    client.change_status(scuript_bot_game, False)
    
    print('Scuript_Bot started successfully.')

#########################################################################################
# Classes

class scuriptlol(zxlolbot.zxLoLBoT):
    def __init__(self, username, password, region="EUW"):
        zxlolbot.zxLoLBoT.__init__(self, username, password, region)
        self.add_event_handler("message", self.on_message)

    def on_message(self, args):
        """Handler for the message event.
        args is a dictionary with specific keys.
        args["sender"]  - The JID of the person the message is coming from.
        args["message"] - The message.
        args["summoner_id"] - The summoner ID of the person the message is coming from."""
        print(args["summoner_id"] + " said " + args["message"])
        self.message(args["sender"], args["message"], False)

    @zxlolbot.botcommand
    def discord(self, sender, args):
        """chat with the glorious milleniumfalcon"""
        self.message(sender, 'Communicating with the milleniumfalcon....')
        client.send_message(client.get_channel(server_id), args)

class game(object):
    def __init__(self, game_name):
        self.set_name(game_name)
    def set_name(self,game_name):
        self.name = game_name

#########################################################################################

#Helper Functions --> should be moved to a utils.py in the utils folder
# Messages
def tutorial(tutorial_channel):
    img_1 = open('../images/tutorial/img_tutorial_000.jpg',"rb")
    img_2 = open('../images/tutorial/img_tutorial_001.jpg',"rb")
    client.send_message(tutorial_channel, "`Guide to setup your sound in Discord. \n1. Check if your microphone is muted \n2. Check if your headphones are deafend \n3. Enter the sound settings`")
    client.send_file(tutorial_channel, img_1)
    client.send_message(tutorial_channel, "`4. Set your sound input and output channels \n5. Activate automatic input sensitivity.`")
    client.send_file(tutorial_channel, img_2)
    client.send_message(tutorial_channel, "`6. Enjoy communicating with other human beeing. \nand remember no cheating. \nBeep Boop SCURIPT_BOT out!`")

# Print a message
def print_message(msg):
    #if msg.content.startswith('!search'):
    #    msg.content = msg.content.replace('!search ', "¡search ")
    client.send_message(msg.channel, "---------------------------------------\n {0} `{1}`\n \t``{2}``".format(msg.author, str(msg.timestamp)[:16], msg.content))
    logger.debug(msg.author)
    logger.debug(msg.content)

# Print a list of messages as one (Char limit = 2000)
def stitch_messages(msgs):
    single_message_array = []
    single_message = 'Search Results:\n'
  #  for i in range(0, len(msgs)):
    for msg in reversed(msgs):
        formated_message = "---------------------------------------\n" + str(msg.author) + '            `' + str(msg.timestamp)[:16] + '`\n \t`' + str(msg.content) + '`\n'
        if len(single_message + formated_message) < 2000:
            single_message = single_message + formated_message
        else:
            single_message_array.append(single_message)
            single_message = formated_message

    single_message_array.append(single_message)

    return single_message_array


# Check if someone is Admin or not.
def is_admin(author):
    if str(author).lower() == 'SirCarfell'.lower() or str(author).lower() == 'ilakarsu'.lower() or str(author).lower == 'SCURIPT_BOT'.lower():
        return True
    else:
        return False


#########################################################################################

if __name__ == "__main__":
    logger.debug('I am in __main__')
    # zxlolbot
    scuriptlol = scuriptlol(username_lol, password_lol)
    scuriptlol.connect()
    scuriptlol.set_status(level=30, status_msg="very scuript, much wow!")


    # discord client
    client.login(username_discord, password_discord)

client.run()