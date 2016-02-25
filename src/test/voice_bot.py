import discord
import configparser


config = configparser.ConfigParser()   
config.read('../cfg/cfg.txt')
username_discord = config.get('scuriptdiscord', 'username_discord')
password_discord = config.get('scuriptdiscord', 'password_discord')

client = discord.Client()
discord.opus.load_opus('libopus-0.dll')


@client.event
async def on_message(message):
	if message.content == '!voice':
		voice_channel = message.author.voice_channel
		print(voice_channel)
		voice = await client.join_voice_channel(voice_channel)
		print(client.is_voice_connected())
		player = voice.create_ffmpeg_player('../../sounds/montage_parodies/MOM GET THE CAMERA.mp3')
		player.start()
		
client.run(username_discord, password_discord)