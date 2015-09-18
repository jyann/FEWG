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

def extract_players(game, playerkey, targetkey):
	return game['players'][playerkey], game['players'][targetkey]

def replace_players(game, playerkey, player, targetkey, target):
	game['players'][playerkey] = player
	game['players'][targetkey] = target

def check_end_game(game):
	if len(game['players'])-len(game['graveyard']) == 1:
		game['winner'] = list(set(game['players'].keys())-set(game['graveyard']))[0]
	elif len(game['players']) == len(game['graveyard']):
		game['winner'] = 'draw'

def incrementKillCount(game, player, targetkey):
	if targetkey not in game['graveyard']:
		# target not already dead
		player['kills'] += 1

# Command functions:

def attack(game, playerkey, targetkey):
	player, target = extract_players(game, playerkey, targetkey)

	subtract(player['stats']['attack'], ['defense','health'], player, target)

	if target['vars']['health'] <= 0:
		incrementKillCount(game, player, targetkey)

		s = set(game['graveyard']) # prevent duplicates
		s.add(targetkey)
		game['graveyard'] = list(s)

	check_end_game(game)

	#return game

def defend(game, playerkey, targetkey):
	player, target = extract_players(game, playerkey, targetkey)

	player['vars']['defense'] += target['stats']['defense']
