from players import Player

valid_commands = ['add_player', 'ready', 'unready']
invalid_names = ['op']

def valid_name(name):
	if (name in invalid_names) or (' ' in name) or (':' in name):
		return False
	else:
		return True

def all_ready(game):
	for flag in game.ready_flags.values():
		if not flag:
			return False

	return True

def add_player(game, name):
	if len(game.players) == game.player_limit:
		return game
	if name in game.players.keys():
		return game

	if valid_name(name):
		game.players[name] = Player()
		game.ready_flags[name] = False

	return game

def ready(game, name):
	game.ready_flags[name] = True
	if all_ready(game):
		game.state = 'running'

	return game

def unready(game, name):
	game.ready_flags[name] = False

	return game