from storage import getPlayer

def newGame(attr):
	"""Get a new game from specified attributes"""
	game = {}
	game['players'] = {}
	game['graveyard'] = []
	game['winner'] = 'NONE'
	return game

def resetPlayer(player):
	"""Reset player data to initial values"""
	player['vars']['health'] = player['stats']['health']
	player['vars']['defense'] = 0

# Command functions:

def login(client, username, password):
	"""Log client in"""
	# Set status
	client.status = 'inlobby'
	# Log in client
	client.name = username
	client.playerdata = getPlayer(username)
	client.factory.named_clients[username] = client

def createGame(client, gamename):
	"""Add game to server"""
	client.factory.games[gamename] = newGame(None)

def joinGame(client, gamename):
	"""Add client to game"""
	# Set status
	client.status = 'ingame'
	# Add client to game
	client.gamekey = gamename
	client.factory.games[gamename]['players'][client.name] = client.playerdata

def quitGame(client):
	"""Remove client from current game"""
	# Set status
	client.status = 'inlobby'
	# Remove client from game
	del client.factory.games[client.gamekey]['players'][client.name]
	if client.name in client.factory.games[client.gamekey]['graveyard']:
		client.factory.games[client.gamekey]['graveyard'].remove(client.name)
	if client.factory.games[client.gamekey]['winner'] == client.name:
		client.factory.games[client.gamekey]['winner'] = 'NONE'
	client.gamekey = None
	# Reset player
	resetPlayer(client.playerdata)

def levelUp(client, statname):
	"""Level player stat"""
	# Set status
	client.status = 'inlobby'
	# Level player up
	client.playerdata['stats'][statname] += 1
	client.playerdata['exp'] -= 1

def logout(client):
	"""Log client out"""
	# Set status
	client.status = 'logging_in'
	# Log client out
	del client.factory.named_clients[client.name]
	client.name = None
