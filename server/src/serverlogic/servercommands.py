from storage import getPlayer

def newGame(game):
	"""Get a new game from specified attributes"""
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
	client.status = 'In lobby'
	# Log in client
	client.name = username
	client.playerdata = getPlayer(username)
	client.factory.named_clients[username] = client

def createGame(client, gamename, attributes):
	"""Add game to server"""
	client.factory.games[gamename] = newGame({'playerlimit':2,'name':gamename})

def joinGame(client, gamename):
	"""Add client to game"""
	# Set status
	client.status = 'In game'
	# Add client to game
	client.gamekey = gamename
	client.factory.games[gamename]['players'][client.name] = client.playerdata

def quitGame(client):
	"""Remove client from current game"""
	# Set status
	client.status = 'In lobby'
	# Reset players
	for ckey in client.factory.games[client.gamekey]['players'].keys():
		resetPlayer(client.factory.named_clients[ckey].playerdata)
	# Remove client from game
	del client.factory.games[client.gamekey]['players'][client.name]
	if client.name in client.factory.games[client.gamekey]['graveyard']:
		client.factory.games[client.gamekey]['graveyard'].remove(client.name)
	if client.factory.games[client.gamekey]['winner'] == client.name:
		client.factory.games[client.gamekey]['winner'] = 'NONE'
	client.gamekey = None

def levelUp(client, statname):
	"""Level player stat"""
	# Set status
	client.status = 'In lobby'
	# Level player up
	client.playerdata['stats'][statname] += 1
	client.playerdata['exp'] -= 1

def logout(client):
	"""Log client out"""
	# Set status
	client.status = 'Logging in'
	# Log client out
	del client.factory.named_clients[client.name]
	client.name = None
