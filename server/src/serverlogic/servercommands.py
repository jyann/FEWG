from storage import getPlayers, getPlayer, storePlayerData

def newGame(game):
	"""Get a new game from specified attributes"""
	game['players'] = {}
	game['graveyard'] = []
	game['winner'] = 'NONE'
	return game

def newPlayer(name, password):
	"""Create player dict"""
	player = {'name':name,'password':password,'stats':{},'vars':{},'exp':0}

	player['stats']['health'] = 10
	player['vars']['health'] = 10

	player['stats']['attack'] = 1
	
	player['stats']['defense'] = 1
	player['vars']['defense'] = 0

	return player

def resetPlayer(player):
	"""Reset player data to initial values"""
	player['vars']['health'] = player['stats']['health']
	player['vars']['defense'] = 0

# Command functions:

def createUser(client, username, password):
	"""Creates a user and stores the player data"""
	path = client.factory.prop_path+'/players.json'
	if username not in getPlayers(path, client.factory.json_decoder):
		storePlayerData(path, username,
					newPlayer(username, password),
					client.factory.json_encoder,
					client.factory.json_decoder)
		return True
	else:
		return False

def login(client, username, password):
	"""Log client in"""
	path = client.factory.prop_path+'/players.json'
	player = getPlayer(path, username, client.factory.json_decoder)
	if player != False and player['password'] == password:
		# Set status
		client.status = 'In lobby'
		# Log in client
		client.name = username
		client.playerdata = player	
		client.factory.named_clients[username] = client
		return True
	else:
		return False

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
	# Store updated player data
	path = client.factory.prop_path+'/players.json'
	storePlayerData(path, username,
				client.playerdata,
				client.factory.json_encoder,
				client.factory.json_decoder)

def logout(client):
	"""Log client out"""
	# Set status
	client.status = 'Logging in'
	# Log client out
	del client.factory.named_clients[client.name]
	client.name = None
