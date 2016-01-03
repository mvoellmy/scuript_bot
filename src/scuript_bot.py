import discord
import getpass
import configparser
from league_functions import get_match_details

# Read cfg.txt
config = configparser.ConfigParser()   
config.read('cfg.txt')
username = config.get('file', 'username')
password = config.get('file', 'password')

# Connect Discord Client
client = discord.Client()
client.login(username, password)


# Messages
def tutorial(tutorial_channel):
    img_1 = open('../images/tutorial/img_tutorial_000.jpg',"rb")
    img_2 = open('../images/tutorial/img_tutorial_001.jpg',"rb")
    client.send_message(tutorial_channel, "`Guide to setup your sound in Discord. \n1. Check if your microphone is muted \n2. Check if your headphones are deafend \n3. Enter the sound settings`")
    client.send_file(tutorial_channel, img_1)
    client.send_message(tutorial_channel, "`4. Set your sound input and output channels \n5. Activate automatic input sensitivity.`")
    client.send_file(tutorial_channel, img_2)
    client.send_message(tutorial_channel, "`6. Enjoy communicating with other human beeing. \nand remember no cheating. \nBeep Boop SCURIPT_BOT out!`")


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
                "!currgame" : "Check if Summoner XY is playing!"} 

    if message.content == '!help':       
        help_msg = "Looks like somebody needs help, lets see what we can do for you! beep-boop:\n \n"
        for k,v in commands.items():
            help_msg+='`{0}`{1}{2}\n'.format(k, placeholder, v)

        client.send_message(message.channel, help_msg)

    if message.content == '!hello':
        client.send_message(message.channel, 'Hello received. Thank you! beep-boop')

    if message.content == '!version':
        client.send_message(message.channel, 'SCURIPT BOT VERSION 0.1!')

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
        summoner_name = message.content.replace('!currgame', "")
        game_details = "Summoner {0} is currently Playing: {1} (EUW)".format(summoner_name, get_match_details(summoner_name).get(queueTypes))
        client.send_message(message.channel, game_details)

# Event for joining members
@client.event
def on_member_join(member):
    server = member.server
    client.send_message(server, 'Welcome {0} to the glorious {1.name} server!'.format(member.mention(), server))
    tutorial(member)

# Commandline output on startup
@client.event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print('ID:')
    print(client.user.id)
    print('------')

client.run()