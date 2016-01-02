import discord

client = discord.Client()
client.login('miro@voellmy.com', 'beep-beep')

tutorial_msg = 'Guide to setup your sound in Discord. \n 1. Check if your microphone is muted \n 2. Check input & output settings \n 3. Activate automatic input sensitivity'

help_msg = '!version \n \n     Displays version of the SCURIPT_BOT \n \n!tutorial \n \n     Guide to setup your sound in Discord'

@client.event
def on_message(message):
    if message.content == '!hello':
        client.send_message(message.channel, 'Hello was received!')

    if message.content == '!version':
        client.send_message(message.channel, 'SCURIPT BOT VERSION 0.1!')

    if message.content == '!tutorial':
        client.send_message(message.channel, tutorial_msg)

    if message.content == '!help':
        client.send_message(message.channel, help_msg)


@client.event
def on_member_join(member):
    server = member.server
    client.send_message(server, 'Welcome {0} to {1.name}!'.format(member.mention(), server))
    client.send_message(member, tutorial_msg )

@client.event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run()