from players import *

valid_commands = ['attack','defend']

def subtract(value, varflow, player, target):
	curval = value
	for varkey in varflow:
		if target['vars'][varkey]-curval < 0:
			curval -= target['vars'][varkey]
			target['vars'][varkey] = 0
		else:
			target['vars'][varkey] -= curval
			break

	#return player, target

def extract_players(game, playerkey, targetkey):
	return game['players'][playerkey], game['players'][targetkey]

def replace_players(game, playerkey, player, targetkey, target):
	game['players'][playerkey] = player
	game['players'][targetkey] = target
	#return game

def check_end_game(game):
	if len(game['players'])-len(game['graveyard']) == 1:
		game['winner'] = list(set(game['players'].keys())-set(game['graveyard']))[0]
	elif len(game['players']) == len(game['graveyard']):
		game['winner'] = 'draw'
	#return game

# Command functions:

def attack(game, playerkey, targetkey):
	player, target = extract_players(game, playerkey, targetkey)

	#player, target = subtract(player['stats']['attack'], ['defense','health'], player, target)
	subtract(player['stats']['attack'], ['defense','health'], player, target)

	if target['vars']['health'] <= 0:
		s =set(game['graveyard']) # prevent duplicates
		s.add(targetkey)
		game['graveyard'] = list(s)

	#game = replace_players(game, playerkey, player, targetkey, target)
	check_end_game(game)

	#return game

def defend(game, playerkey, targetkey):
	player, target = extract_players(game, playerkey, targetkey)

	player['vars']['defense'] += target['stats']['defense']

	#return replace_players(game, playerkey, player, targetkey, target)
