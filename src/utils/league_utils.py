import datetime
import requests
import logging
import configparser



from io import BytesIO
from PIL import Image
from riotwatcher import RiotWatcher
from riotwatcher import EUROPE_WEST
from riotwatcher import NORTH_AMERICA
from riotwatcher import LoLException, error_404, error_429

logger = logging.getLogger("scuript_logger.league")

w = RiotWatcher('b6e57fc8-b03e-40ce-8c84-55d616941248')
#static_champ_list = w.static_get_champion_list()
#logger.debug(static_champ_list)

#CONSTANTS
UNKNOWN = 'unknown'

config = configparser.ConfigParser()
config.read('../cfg/regions.txt')

queue_types = {
    0  : 'CUSTOM',  # Custom games
    2  : 'NORMAL 5x5 BLIND',  # Normal 5v5 blind pick
    8  : 'NORMAL 3x3',  # Normal 3v3 games
    14 : 'NORMAL 5x5 DRAFT',  # Normal 5v5 Draft Pick games
    16 : 'ODIN 5x5 BLIND',  # Dominion 5v5 Blind Pick games
    17 : 'ODIN 5x5 DRAFT',  # Dominion 5v5 Draft Pick games
    4  : 'RANKED SOLO 5x5',  # Ranked Solo 5v5 games
    41 : 'RANKED TEAM 3x3',  # Ranked Team 3v3 games
    42 : 'RANKED TEAM 5x5',  # Ranked Team 5v5 games
    61 : 'TEAM BUILDER 5x5', # Team Builder 5v5 games
    65 : 'ARAM 5x5',  # ARAM games
    70 : 'ONE FOR ALL 5x5', # One for All games
    72 : 'FIRSTBLOOD 1x1', #Snowdown Showdown 1v1 games
    73 : 'FIRSTBLOOD 2x2', #Snowdown Showdown 2v2 games
    75 : 'HEXAKILL 6x6', #Summoner's Rift 6x6 Hexakill games
    76 : 'URF 5x5', #Ultra Rapid Fire games
    83 : 'BOT URF 5x5', #Ultra Rapid Fire games played against AI games
    91 : 'NIGHTMARE BOT 5x5 RANK1', # Doom Bots Rank 1 games
    92 : 'NIGHTMARE BOT 5x5 RANK2', # Doom Bots Rank 2 games
    93 : 'NIGHTMARE BOT 5x5 RANK5', # Doom Bots Rank 5 games
    96 : 'ASCENSION 5x5', # Ascension games
    98 : 'HEXAKILL Twisted Treeline', # Twisted Treeline 6x6 Hexakill games
    100: 'BILGEWATER ARAM 5x5', # Butcher's Bridge games
    300: 'KING PORO 5x5', # Poroking 5v5
    310: 'COUNTER PICK (NEMESIS)', # Nemesis games
    313: 'BILGEWATER 5x5', # Black Market Brawlers games
    999: UNKNOWN #Map is not known or RIOT API didnt provide queue Type ID.	
}

# check if we have API calls remaining
logger.debug('Lets check if we can make requests to the Riot API: ' + str(w.can_make_request()))

# Get Region Parameters out of cfg-file
def get_region_params(region_name):

	region_params = {'Region'    : config.get(region_name, 'region'),
					 'PlatformID': config.get(region_name, 'platformID'),
					 'Domain'    : config.get(region_name, 'domain'),
					 'Port'		 : config.get(region_name, 'port')}
	return region_params

def get_regions():
	return config.sections()


def get_match_details(summoner_name, region_name='EUW'):

	region_params = get_region_params(region_name)
	# w.__init__('b6e57fc8-b03e-40ce-8c84-55d616941248', default_region=region_name)

	match_details = {}

	logger.debug('*********************************************')
	logger.debug('Looking for match details, be patient please:')

	try:
		#fetch summoner and current game info
		summoner = w.get_summoner(name=summoner_name, region=region_params['Region'].lower())
		summoner_id = summoner['id']
		current_game = w.get_current_game(summoner_id, platform_id=region_params['PlatformID'], region=region_params['Region'].lower())
		participants = current_game.get('participants', UNKNOWN)
		logger.debug('Summoner ID: ' + str(summoner_id))
		logger.debug('Game queue ID: ' + str(current_game.get('gameQueueConfigId', 'Error: No gameQueueID.')))
		logger.debug('Game duration in seconds: ' + str(current_game['gameLength']))

		#get queue type infos
		game_queue_id = current_game.get('gameQueueConfigId', 999)
		queue_type = queue_types.get(game_queue_id)
		match_details['queue_type'] = queue_type


		#get game duration
		game_length = current_game.get('gameLength', UNKNOWN)

		match_details['game_length'] = get_seconds_as_time(game_length)

		#get champion info
		champion_id = ''
		for participant in participants:
			if participant.get('summonerId') == summoner_id:				
				champion_id = participant.get('championId', UNKNOWN)

				if champion_id != UNKNOWN:
					champion = w.static_get_champion(champion_id,  champ_data='image')
					image_key = champion.get('image').get('full')
					url = populate_champion_image_url(image_key)

					match_details['champion_name'] = champion.get('name', '')
					match_details['champion_title'] = champion.get('title', '')
					match_details['champion_image'] = url

					logger.debug(champion)

		#ranked stats for current champion
		ranked_stats_champions = w.get_ranked_stats(summoner_id, region=region_params['Region'].lower()).get('champions')
		for rnkd_champ_stat in ranked_stats_champions:
			if rnkd_champ_stat.get('id') == champion_id:
				ranked_stats_current_champion = rnkd_champ_stat.get('stats')
				logger.debug('Ranked stats for current champ: %s', ranked_stats_current_champion)

				games_won = ranked_stats_current_champion.get('totalSessionsWon')
				games_lost = ranked_stats_current_champion.get('totalSessionsLost')

				win_ratio = str(round(int(games_won) / (int(games_won) + int(games_lost)),2) * 100) + '%'

				match_details['games_won'] = games_won
				match_details['games_lost'] = games_lost
				match_details['win_ratio'] = win_ratio

				logger.debug('won: {0} / lost: {1}'.format(games_won,games_lost))
				logger.debug(win_ratio)

		logger.debug(match_details['queue_type'])

		#get encryptionKey for Spectate File
		observers = current_game.get('observers', UNKNOWN)
		match_details['encryption_key'] = observers.get('encryptionKey')
		match_details['game_id'] = current_game.get('gameId', UNKNOWN)



	except LoLException as e:
	    if e == error_429:
	        logger.debug('We should retry in {} seconds.'.format(e.headers['Retry-After']))
	    elif e == error_404:
	        logger.debug('Summoner not found.')

	logger.debug(match_details)
	return match_details


def get_seconds_as_time(gametime_seconds):
	gametime_seconds+=180 #add spectator delay
	hh,mm,ss = str(datetime.timedelta(seconds=gametime_seconds)).split(":")

	duration="{0}:{1}:{2}".format(hh,mm,ss)
	if hh == '0':
		duration="{0}:{1}".format(mm,ss)
	
	return duration

def populate_champion_image_url(champion_key):
	realm_data = w.static_get_realm()
	url_base = realm_data['cdn']
	current_version = realm_data['v']

	return url_base + '/' + current_version + '/img/champion/' + champion_key	