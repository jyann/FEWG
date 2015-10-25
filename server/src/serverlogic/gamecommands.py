valid_commands = ['attack','defend']

def subtract(value, varflow, player, target):
	"""Subtract value from vars in varflow.
	All vars will stay above 0."""
	curval = value
	for varkey in varflow:
		if target['vars'][varkey]-curval < 0:
			curval -= target['vars'][varkey]
			target['vars'][varkey] = 0
		else:
			target['vars'][varkey] -= curval
			break

def extract_players(game, playerkey, targetkey):
	"""Get references to player and target"""
	return game['players'][playerkey], game['players'][targetkey]

def check_end_game(game):
	"""Set winner if game over"""
	if len(game['players'])-len(game['graveyard']) == 1:
		game['winner'] = list(set(game['players'].keys())-set(game['graveyard']))[0]
	elif len(game['players']) == len(game['graveyard']):
		game['winner'] = 'draw'

def incrementKillCount(game, player, targetkey):
	"""Add experience to the player when the target
	is not already in the graveyard."""
	if targetkey not in game['graveyard']:
		# target not already dead
		player['exp'] += 1

# Command functions:

def attack(game, playerkey, targetkey):
	"""Attack command"""
	player, target = extract_players(game, playerkey, targetkey)

	subtract(player['stats']['attack'], ['defense','health'], player, target)

	if target['vars']['health'] <= 0:
		incrementKillCount(game, player, targetkey)

		s = set(game['graveyard']) # prevent duplicates
		s.add(targetkey)
		game['graveyard'] = list(s)

	check_end_game(game)

def defend(game, playerkey, targetkey):
	"""Defend command"""
	player, target = extract_players(game, playerkey, targetkey)

	target['vars']['defense'] += player['stats']['defense']
