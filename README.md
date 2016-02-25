# scuript_bot

SCURIPT_BOT was developed to help new users set up their microphone and headphones propperly.

Join the official SCURIPT_BOT server here:

htttp://discord.me/scuript_bot  

## Usage

    !help

Lists all available commands.

    !join <server_url>

Makes SCURIPT_BOT join your server by executing the following command in the SCURIPT-SERVER found at:
htttp://discord.me/scuript_bot  
The bot is hosted 24/7 and can join your server without the need of any installation! 

    !tutorial

Sends a guide how to setup the microphone and headphones propperly.

    !currgame <summoner_name>

Check if your buddy is playing League of Legends and spectate him!
Options: -<REGION>

    !search <text>

Searches channel history.
Options: -any, -here

    !callouts <MAP_NAME> 

Don't know where 'Tunnels' or 'A-long' is? Enter the CS:GO map name to learn.

    !cleanup <OPTIONS>

Delete the chatlog.
Options: -all, -bot, -cmds, -self

## Installation

Clone this repository and install the needed dependencies.

### Dependencies

Install `python 3.5` from here:

https://www.python.org/

Install the beta of `discord.py` using `pip` and `git`:

    pip install git+https://github.com/Rapptz/discord.py@async

https://github.com/Rapptz/discord.py

Note that this requires `git` to be installed.

Install the Riot API wrapper using pip:

    pip install riotwatcher

https://github.com/pseudonym117/Riot-Watcher

https://developer.riotgames.com/docs/game-constants

https://developer.riotgames.com/docs/spectating-games

Install following packages to run the zxLolBot

    pip install sleekxmpp
    pip install dnspython3

https://github.com/Mathzx/zxLoLBoT

Install `FFmpeg` as instructed here:
    
    http://adaptivesamples.com/how-to-install-ffmpeg-on-windows/

Note that the `Opus Codec` is used for the sounds and the used version is only tested in windows.
    
    https://www.opus-codec.org/

### Setting up your cfg.txt

Add src/cfg.txt with your bots credidentials.

    [scuriptdiscord]
    username_discord = youremail
    password_discord = yourpassword
    
    [scuriptlol]
    username_lol = youraccount
    password_lol = yourpassword

### Let the magic happen

Run in commmand line 

    python scuript_bot.py

or double click

    run_scuript_bot.bat