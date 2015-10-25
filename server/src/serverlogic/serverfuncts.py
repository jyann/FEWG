import logging

import servercommands

# Globals
invalidNames = ['NONE']

logging.basicConfig(level=logging.DEBUG, filename='server.log', format='%(asctime)s | %(message)s')

def logMsg(msg):
	"""Logs the specified message to std out and the file set my the logging config."""
	print msg
	logging.info(msg)

def gamesList(client):
	"""Get list of all games on the server."""
	return [{'name':k,'player_count':len(v['players'])} for k, v in client.factory.games.items()]

def addStatusInfo(client, resp):
	"""Add needed data based on client's status."""
	if client.status == 'inlobby':
		resp['games'] = gamesList(client)
	elif client.status == 'ingame':
		resp['gamedata'] = client.factory.games[client.gamekey]

def sendToLobby(client, resp):
	# Send response to specified clients
	clientlist = [k for k, v in client.factory.named_clients.items() if v.gamekey == None]
	client.factory.sendToClients(clientlist, client.factory.json_encoder.encode(resp))
	# Log
	logMsg('to: '+str(clientlist)+' - '+str(resp))

def sendToGame(client, gamename, resp):
	# Send response to specified clients
	clientlist = client.factory.games[gamename]['players'].keys()
	client.factory.sendToClients(clientlist, client.factory.json_encoder.encode(resp))
	# Log
	logMsg('to: '+str(client.name)+' - '+str(resp))

def sendResp(client, resp):
	# Send response to client
	addStatusInfo(client, resp)
	client.sendMessage(client.factory.json_encoder.encode(resp))
	# Log
	logMsg('to: '+str(client.name)+' - '+str(resp))

def login(client, username, password, sendMsg=True):
	"""Attempt to log client in. 
	Response will contain error response if failed.
	Response will contain lobby data (games) if successful.
	Status changes to 'inlobby' on success."""
	if client.status != 'logging_in':
		logMsg('Login failed: status != logging_in')
		if sendMsg:
			sendResp(client, {'err':'You are already logged in'})
	elif client.name in client.factory.named_clients.keys():
		logMsg('Login failed: client already logged in')
		if sendMsg:
			sendResp(client, {'err':'You are already logged in'})
	elif username in client.factory.named_clients.keys():
		logMsg('Login failed: username conflict')
		if sendMsg:
			sendResp(client, {'err':'That username is already in use'})
	elif username in invalidNames:
		logMsg('Login failed: name not valid')
		if sendMsg:
			sendResp(client, {'err':'That username is not valid, try again'})
	else:
		servercommands.login(client, username, password)
		# Log
		logMsg('Login successful: "'+username+'" logged in')
		if sendMsg:
			sendResp(client, {})

def createGame(client, gamename, sendMsg=True):
	"""Attempt to create a game.
	Response will contain an error message (err) if failed.
	Status does not change on success."""
	if client.name == None:
		logMsg('Create game failed: user not logged in')
		if sendMsg:
			sendResp(client, {'err':'You must be logged in to create a game'})
	elif client.status != 'inlobby':
		logMsg('Create game failed: user not in lobby')
		if sendMsg:
			sendResp(client, {'err':'Must be in lobby to create a game'})
	elif gamename in client.factory.games.keys():
		logMsg('Create game failed: game name conflict')
		if sendMsg:
			sendResp(client, {'err':'That game already exists'})
	elif len(client.factory.games) == client.factory.properties['game_limit']:
		logMsg('Create game failed: game limit reached')
		if sendMsg:
			sendResp(client, {'err':'Game limit reached, try again later or join another game'})
	else:
		servercommands.createGame(client, gamename)
		# Log
		logMsg('Create game successful: "'+gamename+'" created')
		if sendMsg:
			sendToLobby(client, {'games':gamesList(client)})

def joinGame(client, gamename, sendMsg=True):
	"""Attempt to add the client to the specified game.
	Response will contain error message (err) if failed.
	Response will contain game data (gamedata) if successful.
	Status changes to 'ingame' on success."""
	if client.name == None:
		logMsg('Join game failed: client not logged in')
		if sendMsg:
			sendResp(client, {'err':'You must be logged in to join a game'})
	elif client.gamekey != None:
		logMsg('Join game failed: client already in game')
		if sendMsg:
			sendResp(client, {'err':'You are already in a game'})
	elif gamename not in client.factory.games.keys():
		logMsg('Join game failed: no such game')
		if sendMsg:
			sendResp(client, {'err':'There is currently no game with that name'})
	else:
		servercommands.joinGame(client, gamename)
		# Log
		logMsg('Join game successful: "'+client.name+'"added to "'+gamename+'"')
		if sendMsg:
			sendToGame(client, gamename, {'gamedata':client.factory.games[gamename]})

def quitGame(client, sendMsg=True):
	"""Attempt to quit game.
	Response will contain error message (err) if failed.
	Response will contain lobby data (games) if successful.
	Status changes to 'inlobby' on success."""
	if client.gamekey == None:
		logMsg('Quit game failed: client not in game')
		if sendMsg:
			sendResp(client, {'err':'You are not in a game yet'})
	else:
		# Capture game name
		gamename = client.gamekey

		servercommands.quitGame(client)
		# Log
		logMsg('Quit game successful: "'+client.name+'" removed from "'+gamename+'"')
		if sendMsg:
			sendToGame(client, gamename, {'gamedata':client.factory.games[gamename]})
			sendResp(client, {})

def levelup(client, statname, sendMsg=True):
	"""Attempt to level up player.
	Response will contain error message (err) if failed.
	Response will contain lobby data (games) if successful.
	Status changes to 'inlobby' on success."""
	if client.playerdata == None:
		logMsg('Level up failed: client not logged in')
		if sendMsg:
			sendResp(client, {'err':'You must be logged in to level up'})
	elif statname not in client.playerdata['stats'].keys():
		logMsg('Level up failed: no such stat')
		if sendMsg:
			sendResp(client, {'err':"Couldn't find that stat, try another again"})
	elif client.playerdata['exp'] <= 0:
		logMsg('Level up failed: not enough exp')
		if sendMsg:
			sendResp(client, {'err':"You don't have enough XP, win some games first"})
	else:
		servercommands.levelUp(client, statname)
		# Log
		logMsg('Level up successful: "'+statname+'" increased by 1 for "'+client.name+'"')
		if sendMsg:
			sendResp(client, {})

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
			sendResp(client, {'err':"You haven't logged in yet"})
	else:
		# Capture username
		username = client.name

		servercommands.logout(client)
		# Log
		logMsg('Logout successful: "'+username+'" logged out')
		if sendMsg:
			sendResp(client, {'status':'logged_out'})

def closeConn(client):
	"""Remove client data and close connection with client"""
	logMsg('Closing client connection')
	# Clear client data
	logout(client, False)
	client.factory.clients.remove(client)
	# Disconnect
	client.abortConnection()
