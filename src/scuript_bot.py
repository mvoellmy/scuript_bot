#imports
import sys
sys.path.append('utils/')

import scuriptdiscord, scuriptlol
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

## SCURIPT BOT ##
logging.config.fileConfig('../cfg/logging.conf')
logger = logging.getLogger("scuript_logger.main")

# Read cfg.txt
config = configparser.ConfigParser()   
config.read('../cfg/cfg.txt')

username_discord = config.get('scuriptdiscord', 'username_discord')
password_discord = config.get('scuriptdiscord', 'password_discord')

username_lol = config.get('scuriptlol', 'username_lol')
password_lol = config.get('scuriptlol', 'password_lol')


if __name__ == "__main__":
    logger.debug('Starting scuript bot ...beep-boop.')

    # zxlolbot
    scuriptlol = scuriptlol.scuriptlol(username_lol, password_lol)
    scuriptlol.connect()


    # discord client
    scuriptdiscord = scuriptdiscord.scuriptdiscord(username_discord, password_discord)
    scuriptdiscord.client.run(username_discord, password_discord)