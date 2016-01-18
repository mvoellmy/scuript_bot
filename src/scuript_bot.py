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

from collections import deque
from decimal import Decimal

# Scuript Modules
from league_utils import get_match_details

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

member_join = True

#########################################################################################
# TODO add all discord related code to the scuriptdiscord class
# Commands for the bot
@client.event
def on_message(message):
    placeholder = "\n \t"
    commands =  {"!help"    : "Displays version of the SCURIPT_BOT", 
                "!version"  : "Look up the current version of scuript_bot!.", 
                "!hello"    : "Say 'Hello' to scuript_bot!", 
                "!tutorial" : "Guide to setup your sound in Discord", 
                "!join"     : "enter your (SERVER_URL)", 
                "!git"      : "Link to the github repo.", 
                "!tts"      : "Let the bot speak for you!",
                "!rekt"     : "Get R3kt son!",
                "!currgame" : "Check if Summoner XY is playing and for how long!",
                "!search"   : "Search the messages sent since the bot has been started."}

    if message.content == '!sclol':
        print('I will try to send this to summoner: @fox3ye')
        #todo send this message to summoner....

    if message.content == '!help':
        help_msg = "Looks like somebody needs help, lets see what we can do for you! beep-boop:\n \n"
        for k,v in commands.items():
            help_msg+='`{0}`{1}{2}\n'.format(k, placeholder, v)

        client.send_message(message.channel, help_msg)

    if message.content == '!hello':
        client.send_message(message.channel, 'Hello received. Thank you! beep-boop')

    if message.content == '!version':
        client.send_message(message.channel, 'SCURIPT BOT VERSION 0.0.3!')

    if message.content == '!tutorial':
        tutorial(message.channel)

    if message.content.startswith('!join'):
        url = message.content.replace("!join ", "")
        client.accept_invite(url)
        client.send_message(message.channel, "SCURIPT_BOT successfully joined your channel!")
    
    if message.content == '!git':
        client.send_message(message.channel, 'https://github.com/mvoellmy/scuript_bot')

    if message.content.startswith('!tts'):
        tts_msg = message.content.replace("!tts ", "")
        tts_msg = 'Beep, boop. ' + tts_msg + '. Beep, boop.'
        client.send_message(message.channel, tts_msg, True, True)

    if message.content.startswith('!rekt'):
        tts_msg = 'You have been rekt!'
        client.send_message(message.channel, tts_msg, True, True)

    if message.content.startswith('!currgame'):
        summoner_name = message.content.replace('!currgame ', "")
        match_details = get_match_details(summoner_name)

        show_champion_details = False
        if not match_details:
            game_details = "`Summoner '{0}' is currently not in a game..`".format(summoner_name)

        elif match_details.get('queue_type') == 'unknown' and match_details.get('game_length') == 'unknown':
           game_details = "`Are you sure summoner: '{0}', is currently ingame?`".format(summoner_name)   

        elif match_details.get('queue_type') == 'unknown':
            show_champion_details = True
            client.send_message(message.channel, match_details.get('champion_image'))
            game_details = "`Summoner '{0}' appears to be ingame as {1} {2} on (EUW) for {3} minutes. But unfortunately the game mode is: {4} :(.`".format(summoner_name, match_details.get('champion_name'), match_details.get('champion_title'), match_details.get('game_length'), match_details.get('queue_type'))
        
        else:
            show_champion_details = True
            client.send_message(message.channel, match_details.get('champion_image'))
            game_details = "`Summoner '{0}' is currently playing {1} {2}: {3} (EUW) for {4} minutes.`".format(summoner_name, match_details.get('champion_name'), match_details.get('champion_title'), match_details.get('queue_type'), match_details.get('game_length'))
            

        client.send_message(message.channel, game_details)

        if show_champion_details:
            client.send_message(message.channel, "`\n \t Ranked stats with: {0}\n \t won: {1}\n \t lost: {2}\n \t ratio: {3}`".format(match_details.get('champion_name'), match_details.get('games_won'), match_details.get('games_lost'), match_details.get('win_ratio')))
            # Specatate Mode encryption key
            spectate_file_stream = open('op_gg_spectate_template.bat','r')
            spectate_file_content = spectate_file_stream.read()
            spectate_file_stream.close()
            # Add correct encryption_key and game_id to bat file
            spectate_file_content = spectate_file_content.replace("encryptionKeyPlaceholder", match_details.get('encryption_key'))           
            spectate_file_content = spectate_file_content.replace("gameIdPlaceholder", str(match_details.get('game_id')))           

            spectate_file_stream = open('op_gg_spectate_customized.bat','w')
            spectate_file_stream.write(spectate_file_content)
            spectate_file_stream.close()
            
            op_gg_bat = open('op_gg_spectate_customized.bat',"rb")
            client.send_message(message.channel, 'Spectate the game by downloading and opening the following file:')          
            client.send_file(message.channel, op_gg_bat)
            # client.send_message(message.channel, 'Yes, Windows thinks its unsafe. \nNo, it is no virus. ;)')          



    if message.content.startswith('!search') and str(message.author).lower() != 'SCURIPT_BOT'.lower():
        number_of_requests = 10;
        result_count = 0
        search_count = 0
        search_msg = message.content.replace('!search ', "")
        before_msg = message
        results = []


        for request in range(0, number_of_requests):
            search_messages = client.logs_from(message.channel, 100, before_msg)
            for it_msg in search_messages:
                search_count = search_count + 1
                if str(search_msg).lower() in str(it_msg.content).lower() and str(it_msg.author).lower() != 'SCURIPT_BOT'.lower() and it_msg.content.startswith('!') is not True:
                    results.append(it_msg)
                    result_count = result_count + 1
            before_msg = it_msg

        client.send_message(message.channel,"{0} matching results have been found! ({0}/{1})".format(result_count, search_count))        
        
        #Print results as single messages
        for i in range(0, len(results)):
            print_message(results[i])
            time.sleep(1)

        #Print results as one big message
        #client.send_message(message.channel,stitch_messages(results))

        client.send_message(message.channel,"---------------------------------------\nSuccessfully displayed all {0} messages. Beep-Boop".format(result_count))

    if message.content.startswith('!mbr_join') and str(message.author).lower == 'SirCarfell'.lower():
        search_msg = message.content.replace('!mbr_join ', "")
        if search_msg == 0:
            member_join = False
            client.send_message(message.channel,"Turned welcome messages off.")
        elif search_msg == 1:
            member_join = True
            client.send_message(message.channel,"Turned welcome messages on.")
        else:
            client.send_message(message.channel,"Unvalid mbr_join argument.")

 

#emotes(message)
#'''def emotes(message):
#    emote = open('../images/emotes/',"rb")
#    client.send_message(tutorial_channel, "`Guide to setup your sound in Discord. \n1. Check if your microphone is muted \n2. Check if your headphones are deafend \n3. Enter the sound settings`")
#    client.send_file(tutorial_channel, img_1)'''
 

# Event for joining members
@client.event
def on_member_join(member):
    if member_join == True:
        server = member.server
        client.send_message(server, 'Welcome {0} to the glorious {1.name} server!'.format(member.mention(), server))
        tutorial(member)

# Commandline output on startup
@client.event
def on_ready():
    logger.debug('Logged in as')
    logger.debug(client.user.name)
    logger.debug('ID:')
    logger.debug(client.user.id)
    logger.debug('------')

#########################################################################################

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
    client.send_message(msg.channel, "---------------------------------------\n{0}            `{1}`\n \t``{2}``".format(msg.author, str(msg.timestamp)[:16], msg.content))
    logger.debug(msg.author)
    logger.debug(msg.content)

# Print a list of messages as one (Char limit = 2000)
def stitch_messages(msgs):
    single_message = 'Search Results:\n'
    for i in range(0, len(msgs)):
        msg = msgs[i]
        single_message = single_message +'``'+ str(msg.author) + '``    ``' +  str(msg.timestamp) + '``\n' + str(msg.content) + '\n'
    return single_message

#########################################################################################

if __name__ == "__main__":
    # zxlolbot
    scuriptlol = scuriptlol(username_lol, password_lol)
    scuriptlol.connect()
    scuriptlol.set_status(level=30, status_msg="very scuript, much wow!")

    # discord client
    client.login(username_discord, password_discord)
    client.run()