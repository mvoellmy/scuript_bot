import discord
import getpass
import configparser

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

help_msg = '`!version` \n \n \tDisplays version of the SCURIPT_BOT \n \n`!tutorial` \n \n \tGuide to setup your sound in Discord \n \n `!join (SERVER_URL)` \n \n \tMake SCURIPT_BOT join your server!'

# Commands for the bot
@client.event
def on_message(message):
    if message.content == '!hello':
        client.send_message(message.channel, 'Hello was received!')

    if message.content == '!version':
        client.send_message(message.channel, 'SCURIPT BOT VERSION 0.1!')

    if message.content == '!tutorial':
        tutorial(message.channel)

    if message.content == '!help':
        client.send_message(message.channel, help_msg)

    if message.content.startswith('!join'):
        url = message.content.replace("!join ", "")
        client.accept_invite(url)
        client.send_message(message.channel, "SCURIPT_BOT successfully joined your channel!")


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