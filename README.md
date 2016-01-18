# scuript_bot

SCURIPT_BOT was developed to help new users set up their microphone and headphones propperly.

## Usage

    !join <server_url>

Makes SCURIPT_BOT join your server by executing the following command in the SCURIPT-SERVER found at:

htttp://discord.me/scuript_bot	

    !tutorial

Sends a guide how to setup the microphone and headphones propperly.

    !search <text>

Searches channel history.

    !help

Lists all available commands.

    !currgame <summoner_name>

League of Legends: Shows details to currently active game (EUW only atm)

## Installation

Clone this repository and install the needed dependencies.

### Dependencies

Install python 3.5 from here:

https://www.python.org/

Install the discord python wrapper using pip:

    pip install discord.py

https://github.com/Rapptz/discord.py

Install the Riot API wrapper using pip:

    pip install riotwatcher

https://github.com/pseudonym117/Riot-Watcher

https://developer.riotgames.com/docs/game-constants

https://developer.riotgames.com/docs/spectating-games

Pillow is also needed

    pip install sleekxmpp
    pip install dnspython3
    
### Setting up your cfg.txt

Add src/cfg.txt with your bots credidentials.


    [scuriptdiscord]
    username_discord = youremail
    password_discord = yourpassword
    
    [scuriptlol]
    username_lol = youraccount
    password_lol = yourpassword

### Let the magic happen

Run 

    python scuript_bot.py
