valid_waiting_room_commands = ['add_player', 'ready', 'unready']

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

	game.players[name] = Player()
	game.ready_flags[name] = False

	return game

def ready(game, name):
	game.ready_flags[name] = True
	if game.all_ready():
		game.state = 'running'

def unready(game, name):
	game.ready_flags[name] = False