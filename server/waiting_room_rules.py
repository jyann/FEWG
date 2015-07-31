from players import Player

valid_commands = ['add_player', 'ready', 'unready']
invalid_keys = ['op']

def valid_key(playerkey):
	if (playerkey in invalid_keys) or (' ' in playerkey) or (':' in playerkey):
		return False
	else:
		return True

def all_ready(game):
	for player in game.players.values():
		if player.status != 'ready':
			return False

	return True

# Command functions:

def add_player(game, playerkey, targetkey):
	if len(game.players) == game.player_limit:
		return game
	if playerkey in game.players.keys():
		return game

	if valid_key(playerkey):
		game.players[playerkey] = Player()

	return game

def ready(game, playerkey, targetkey):
	game.players[playerkey].status = 'ready'
	if all_ready(game):
		game.state = 'running'

	return game

def unready(game, playerkey, targetkey):
	game.ready_flags[playerkey] = False

	return game