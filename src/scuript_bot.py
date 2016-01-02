import discord

client = discord.Client()
client.login('miro@voellmy.com', 'beep-beep')

@client.event
def on_message(message):
    if message.content.startswith('!hello'):
        client.send_message(message.channel, 'Hello was received!')
    if message.content.startswith('!version'):
        client.send_message(message.channel, 'SCURIPT BOT VERSION 0.1!')

@client.event
def on_member_join(member):
    server = member.server
    client.send_message(member.user, 'Welcome {0} to {1.name}!'.format(member.mention(), server))

@client.event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run()