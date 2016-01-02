import discord

client = discord.Client()
client.login('miro@voellmy.com', 'beep-beep')

@client.event
def on_message(message):
    if message.content.startswith('!hello'):
        client.send_message(message.channel, 'Hello was received!')

@client.event
def on_message(message):
    if message.content.startswith('!version'):
        client.send_message(message.channel, 'SCURIPT BOT VERSION 0.1!')


@client.event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run()