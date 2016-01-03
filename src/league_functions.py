from riotwatcher import RiotWatcher
from riotwatcher import EUROPE_WEST
from riotwatcher import LoLException, error_404, error_429

w = RiotWatcher('b6e57fc8-b03e-40ce-8c84-55d616941248', default_region=EUROPE_WEST)


queue_types = {
    0 : 'CUSTOM',  # Custom games
    2 : 'NORMAL 5x5 BLIND',  # Normal 5v5 blind pick
    8 : 'NORMAL 3x3',  # Normal 3v3 games
    14 : 'NORMAL 5x5 DRAFT',  # Normal 5v5 Draft Pick games
    4 : 'RANKED SOLO 5x5',  # Ranked Solo 5v5 games
    41 : 'RANKED TEAM 3x3',  # Ranked Team 3v3 games
    42 : 'RANKED TEAM 5x5',  # Ranked Team 5v5 games
    65 : 'ARAM 5x5',  # ARAM games
}

# check if we have API calls remaining
#if w.can_make_request()==False:
#	print('Woops, unfortunately the Riot API does not accept any requests at the moment!')


def get_match_details(summoner_name):
	try:
		summoner = w.get_summoner(name=summoner_name)
		print(summoner)

		current_game = w.get_current_game(summoner['id'])
		queueType = queue_types.get(current_game['gameQueueConfigId'])
		print(queueType)

	except LoLException as e:
	    if e == error_429:
	        print('We should retry in {} seconds.'.format(e.headers['Retry-After']))
	    elif e == error_404:
	        print('Summoner not found.')

	return queueType	