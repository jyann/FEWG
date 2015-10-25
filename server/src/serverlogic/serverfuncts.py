import logging

from storage import getPlayer

# Globals
invalidNames = ['NONE']

logging.basicConfig(level=logging.DEBUG, filename='server.log', format='%(asctime)s | %(message)s')

def logMsg(msg):
	"""Logs the specified message to std out and the file set my the logging config."""
	print msg
	logging.info(msg)

def resetPlayer(player):
	"""Reset player data to initial values."""
	player['vars']['health'] = player['stats']['health']
	player['vars']['defense'] = 0

def gamesList(client):
	"""Get list of all games on the server."""
	return [{'name':k,'player_count':len(v['players'])} for k, v in client.factory.games.items()]

def addStatusInfo(client, resp):
	"""Add needed data based on client's status."""
	if client.status == 'inlobby':
		resp['games'] = gamesList(client)
	elif client.status == 'ingame':
		resp['gamedata'] = client.factory.games[client.gamekey]

def login(client, username, password, sendMsg=True):
	"""Attempt to log client in. 
	Response will contain error response if failed.
	Response will contain lobby data (games) if successful.
	Status changes to 'inlobby' on success."""
	if client.status != 'logging_in':
		logMsg('Login failed: status != logging_in')
		if sendMsg:
			# Send response to client
			resp = {}
			resp['err'] = 'You are already logged in'
			addStatusInfo(client, resp)
			client.sendMessage(client.factory.json_encoder.encode(resp))
			# Log
			logMsg('to: '+str(client.name)+' - '+str(resp))
	elif client.name in client.factory.named_clients.keys():
		logMsg('Login failed: client already logged in')
		if sendMsg:
			# Send response to client
			resp = {}
			resp['err'] = 'You are already logged in'
			client.sendMessage(client.factory.json_encoder.encode(resp))
			# Log
			logMsg('to: '+str(client.name)+' - '+str(resp))
	elif username in client.factory.named_clients.keys():
		logMsg('Login failed: username conflict')
		if sendMsg:
			# Send response to client
			resp = {}
			resp['err'] = 'That username is already in use'
			client.sendMessage(client.factory.json_encoder.encode(resp))
			# Log
			logMsg('to: '+str(client.name)+' - '+str(resp))
	elif username in invalidNames:
		logMsg('Login failed: name not valid')
		if sendMsg:
			# Send response to client
			resp = {}
			resp['err'] = 'That username is not valid, try again'
			client.sendMessage(client.factory.json_encoder.encode(resp))
			# Log
			logMsg('to: '+str(client.name)+' - '+str(resp))
	else:
		# Set status
		client.status = 'inlobby'
		# Log in client
		client.name = username
		client.playerdata = getPlayer(username)
		client.factory.named_clients[username] = client
		# Log
		logMsg('Login successful: "'+username+'" logged in')
		if sendMsg:
			# Send response to client
			resp = {}
			addStatusInfo(client, resp)
			client.sendMessage(client.factory.json_encoder.encode(resp))
			# Log
			logMsg('to: '+str(client.name)+' - '+str(resp))

def newGame(attr):
	"""Get a new game from specified attributes."""
	game = {}
	game['players'] = {}
	game['graveyard'] = []
	game['winner'] = 'NONE'
	return game

def createGame(client, gamename, sendMsg=True):
	"""Attempt to create a game.
	Response will contain an error message (err) if failed.
	Status does not change on success."""
	if client.name == None:
		logMsg('Create game failed: user not logged in')
		if sendMsg:
			# Send response to client
			resp = {}
			resp['err'] = 'You must be logged in to create a game'
			addStatusInfo(client, resp)
			client.sendMessage(client.factory.json_encoder.encode(resp))
			# Log
			logMsg('to: '+str(client.name)+' - '+str(resp))
	elif client.status != 'inlobby':
		logMsg('Create game failed: user not in lobby')
		if sendMsg:
			# Send response to client
			resp = {}
			resp['err'] = 'Must be in lobby to create a game'
			addStatusInfo(client, resp)
			client.sendMessage(client.factory.json_encoder.encode(resp))
			# Log
			logMsg('to: '+str(client.name)+' - '+str(resp))
	elif gamename in client.factory.games.keys():
		logMsg('Create game failed: game name conflict')
		if sendMsg:
			# Send response to client
			resp = {}
			resp['err'] = 'That game already exists'
			addStatusInfo(client, resp)
			client.sendMessage(client.factory.json_encoder.encode(resp))
			# Log
			logMsg('to: '+str(client.name)+' - '+str(resp))
	elif len(client.factory.games) == client.factory.properties['game_limit']:
		logMsg('Create game failed: game limit reached')
		if sendMsg:
			# Send response to client
			resp = {}
			resp['err'] = 'Game limit reached, try again later or join another game'
			addStatusInfo(client, resp)
			client.sendMessage(client.factory.json_encoder.encode(resp))
			# Log
			logMsg('to: '+str(client.name)+' - '+str(resp))
	else:
		client.factory.games[gamename] = newGame(None)
		logMsg('Create game successful: "'+gamename+'" created')
		if sendMsg:
			# Send response to specified clients
			clientlist = [k for k, v in client.factory.named_clients.items() if v.gamekey == None]
			resp = {}
			addStatusInfo(client, resp)
			client.factory.sendToClients(clientlist, client.factory.json_encoder.encode(resp))
			# Log
			logMsg('to: '+str(clientlist)+' - '+str(resp))

def joinGame(client, gamename, sendMsg=True):
	"""Attempt to add the client to the specified game.
	Response will contain error message (err) if failed.
	Response will contain game data (gamedata) if successful.
	Status changes to 'ingame' on success."""
	if client.name == None:
		logMsg('Join game failed: client not logged in')
		if sendMsg:
			# Send response to client
			resp = {}
			resp['err'] = 'You must be logged in to join a game'
			addStatusInfo(client, resp)
			client.sendMessage(client.factory.json_encoder.encode(resp))
			# Log
			logMsg('to: '+str(client.name)+' - '+str(resp))
	elif client.gamekey != None:
		logMsg('Join game failed: client already in game')
		if sendMsg:
			# Send response to client
			resp = {}
			resp['err'] = 'You are already in a game'
			addStatusInfo(client, resp)
			client.sendMessage(client.factory.json_encoder.encode(resp))
			# Log
			logMsg('to: '+str(client.name)+' - '+str(resp))
	elif gamename not in client.factory.games.keys():
		logMsg('Join game failed: no such game')
		if sendMsg:
			# Send response to client
			resp = {}
			resp['err'] = 'There is currently no game with that name'
			addStatusInfo(client, resp)
			client.sendMessage(client.factory.json_encoder.encode(resp))
			# Log
			logMsg('to: '+str(client.name)+' - '+str(resp))
	else:
		# Set status
		client.status = 'ingame'
		# Add client to game
		client.gamekey = gamename
		client.factory.games[gamename]['players'][client.name] = client.playerdata
		# Log
		logMsg('Join game successful: "'+client.name+'"added to "'+gamename+'"')
		if sendMsg:
			# Send response to specified clients
			clientlist = client.factory.games[client.gamekey]['players'].keys()
			resp = {}
			addStatusInfo(client, resp)
			client.factory.sendToClients(clientlist, client.factory.json_encoder.encode(resp))
			# Log
			logMsg('to: '+str(client.name)+' - '+str(resp))

def quitGame(client, sendMsg=True):
	"""Attempt to quit game.
	Response will contain error message (err) if failed.
	Response will contain lobby data (games) if successful.
	Status changes to 'inlobby' on success."""
	if client.gamekey == None:
		logMsg('Quit game failed: client not in game')
		if sendMsg:
			# Send response to client
			resp = {}
			resp['err'] = 'You are not in a game yet'
			addStatusInfo(client, resp)
			client.sendMessage(client.factory.json_encoder.encode(resp))
			# Log
			logMsg('to: '+str(client.name)+' - '+str(resp))
	else:
		# Set status
		client.status = 'inlobby'
		# Capture game name
		gamename = client.gamekey
		# Remove client from game
		del client.factory.games[gamename]['players'][client.name]
		if client.name in client.factory.games[gamename]['graveyard']:
			client.factory.games[gamename]['graveyard'].remove(client.name)
		if client.factory.games[gamename]['winner'] == client.name:
			client.factory.games[gamename]['winner'] = 'NONE'
		client.gamekey = None
		# Reset player
		resetPlayer(client.playerdata)
		# Log
		logMsg('Quit game successful: "'+client.name+'" removed from "'+gamename+'"')
		if sendMsg:
			# Send response to specified clients
			clientlist = client.factory.games[gamename]['players'].keys()
			resp = {}
			resp['gamedata'] = client.factory.games[gamename]
			msg = client.factory.json_encoder.encode(resp)
			client.factory.sendToClients(clientlist, msg)
			# Log
			logMsg('to: '+str(clientlist)+' - '+str(resp))
			# Send response to client
			resp = {}
			resp['games'] = gamesList(client)
			client.sendMessage(client.factory.json_encoder.encode(resp))
			# Log
			logMsg('to: '+str(client.name)+' - '+str(resp))

def levelup(client, statname, sendMsg=True):
	"""Attempt to level up player.
	Response will contain error message (err) if failed.
	Response will contain lobby data (games) if successful.
	Status changes to 'inlobby' on success."""
	if client.playerdata == None:
		logMsg('Level up failed: client not logged in')
		if sendMsg:
			# Send response to client
			resp = {}
			resp['err'] = 'You must be logged in to level up'
			addStatusInfo(client, resp)
			client.sendMessage(client.factory.json_encoder.encode(resp))
			# Log
			logMsg('to: '+str(client.name)+' - '+str(resp))
	if statname not in client.playerdata['stats'].keys():
		logMsg('Level up failed: no such stat')
		if sendMsg:
			# Send response to client
			resp = {}
			resp['err'] = "Couldn't find that stat, try another again"
			addStatusInfo(client, resp)
			client.sendMessage(client.factory.json_encoder.encode(resp))
			# Log
			logMsg('to: '+str(client.name)+' - '+str(resp))
	if client.playerdata['exp'] <= 0:
		logMsg('Level up failed: not enough exp')
		if sendMsg:
			# Send response to client
			resp = {}
			resp['err'] = "You don't have enough XP, win some games first"
			addStatusInfo(client, resp)
			client.sendMessage(client.factory.json_encoder.encode(resp))
			# Log
			logMsg('to: '+str(client.name)+' - '+str(resp))
	else:
		# Set status
		client.status = 'inlobby'
		# Level player up
		client.playerdata['stats'][statname] += 1
		client.playerdata['exp'] -= 1
		# Log
		logMsg('Level up successful: "'+statname+'" increased by 1 for "'+client.name+'"')
		if sendMsg:
			# Send response to client
			resp = {}
			resp['games'] = gamesList(client)
			client.sendMessage(client.factory.json_encoder.encode(resp))
			# Log
			logMsg('to: '+str(client.name)+' - '+str(resp))

def logout(client, sendMsg=True):
	"""Attempt to log client out.
	Response will contain error message (err) if failed.
	Response will contain if status of 'logged_out' successful.
	Status changes to 'logging_in' on success."""
	# Clear game data
	quitGame(client, False)

	if client.name == None:
		logMsg('Logout failed: client not logged in')
		if sendMsg:
			# Send response to client
			resp = {}
			resp['err'] = "You haven't logged in yet"
			client.sendMessage(client.factory.json_encoder.encode(resp))
			# Log
			logMsg('to: '+str(client.name)+' - '+str(resp))
	else:
		# Set status
		client.status = 'logging_in'
		# Capture username
		usrname = client.name
		# Log client out
		del client.factory.named_clients[client.name]
		client.name = None
		# Log
		logMsg('Logout successful: "'+usrname+'" logged out')
		if sendMsg:
			# Send response to client
			resp = {}
			resp['status'] = 'logged_out'
			client.sendMessage(client.factory.json_encoder.encode(resp))
			# Log
			logMsg('to: '+str(client.name)+' - '+str(resp))

def closeConn(client):
	"""Remove client data and close connection with client"""
	logMsg('Closing client connection')
	# Clear client data
	logout(client, False)
	client.factory.clients.remove(client)
	# Disconnect
	client.abortConnection()
