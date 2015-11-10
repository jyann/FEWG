import logging

import servercommands

# Globals
invalidNames = ['NONE']

def configLog(filepath):
	logging.basicConfig(level=logging.DEBUG, 
		filename=filepath, 
		format='%(asctime)s | %(message)s')

def logMsg(msg):
	"""Logs the specified message to std out 
	and the file set my the logging config."""
	print msg
	logging.info(msg)

def gamesList(client):
	"""Get list of all games on the server."""
	return [{'name':k,
			'player_count':len(v['players']),
			'playerlimit':v['playerlimit']} 
			for k, v in client.factory.games.items()]

def addStatusInfo(client, resp):
	"""Add needed data based on client's status."""
	resp['status'] = client.status
	if client.status == 'In lobby':
		resp['games'] = gamesList(client)
	elif client.status == 'In game':
		resp['gamedata'] = client.factory.games[client.gamekey]

def sendToLobby(client, resp):
	"""Send response to specified clients"""
	clientlist = [k for k, v 
			in client.factory.named_clients.items() 
			if v.gamekey == None]
	resp['status'] = 'In lobby'
	resp['games'] = gamesList(client)
	client.factory.sendToClients(clientlist, 
			client.factory.json_encoder.encode(resp))
	# Log
	logMsg('to: '+str(clientlist)+' - '+str(resp))

def sendToGame(client, gamename, resp):
	"""Send response to specified clients"""
	clientlist = client.factory.games[gamename]['players'].keys()
	resp['status'] = 'In game'
	resp['gamedata'] = client.factory.games[gamename]
	client.factory.sendToClients(clientlist, 
			client.factory.json_encoder.encode(resp))
	# Log
	logMsg('to: '+str(clientlist)+' - '+str(resp))

def sendResp(client, resp):
	"""Send response to client"""
	addStatusInfo(client, resp)
	client.sendMessage(client.factory.json_encoder.encode(resp))
	# Log
	logMsg('to: '+str(client.name)+' - '+str(resp))

def sendError(client, error):
	"""Send client an error"""
	logMsg('Client error: '+error)
	sendResp(client, {'err':error})

# Command functions:

def createUser(client, cmd, sendMsg=True):
	"""Create a new user and save new player data"""
	if len(cmd) < 4:
		if sendMsg:
			sendError(client, 'Both username and password are required')
	elif len(cmd) > 4 or cmd[2] in invalidNames:
		if sendMsg:
			sendError(client, 'Invalid username or password')
	elif servercommands.createUser(client, cmd[2], cmd[3]):
		if sendMsg:
			sendResp(client, {'message':'User successfully created'})
	else:
		if sendMsg:
			sendError(client, 'Failed to create user')

def login(client, cmd, sendMsg=True):
	"""Attempt to log client in. 
	Response will contain error response if failed.
	Response will contain lobby data (games) if successful.
	Status changes to 'inlobby' on success."""
	if len(cmd) < 3:
		if sendMsg:
			sendError(client, 'Both username and password required')
		return
	elif len(cmd) > 3:
		if sendMsg:
			sendError(client, 'Invalid username or password')
		return
	else:
		username, password = cmd[1], cmd[2]

	if client.status != 'Logging in':
		if sendMsg:
			sendError(client, 'You are already logged in')
	elif client.name in client.factory.named_clients.keys():
		if sendMsg:
			sendError(client, 'You are already logged in')
	elif username in client.factory.named_clients.keys():
		if sendMsg:
			sendError(client, 'That username is already in use')
	elif username in invalidNames:
		if sendMsg:
			sendError(client, 'That username is not valid, try again')
	else:
		if servercommands.login(client, username, password):
			# Log
			logMsg('Login successful: "'+username+'" logged in')
			if sendMsg:
				sendResp(client, {'message':'Logged in as '+username})
		else:
			if sendMsg:
				sendError(client, 'Invalid username or password')

def createGame(client, cmd, sendMsg=True):
	"""Attempt to create a game.
	Response will contain an error message (err) if failed.
	Status does not change on success."""
	error = None

	if len(cmd) != 3:
		if sendMsg:
			sendError(client, 'No game name provided')
		return
	else:
		gamename = cmd[2]

	if client.name == None:
		if sendMsg:
			sendError(client, 'You must be logged in to create a game')
	elif client.status != 'In lobby':
		if sendMsg:
			sendError(client, 'Must be in lobby to create a game')
	elif gamename in client.factory.games.keys():
		if sendMsg:
			sendError(client, 'That game already exists')
	elif (len(client.factory.games) 
			== int(client.factory.properties['game_limit'])):
		if sendMsg:
			sendError(client, """Game limit reached, 
					try again later or join another game""")
	else:
		servercommands.createGame(client, gamename, {})
		# Log
		logMsg('Create game successful: "'+gamename+'" created')
		if sendMsg:
			sendToLobby(client, {'message':'Game '+gamename+' created'})

def joinGame(client, cmd, sendMsg=True):
	"""Attempt to add the client to the specified game.
	Response will contain error message (err) if failed.
	Response will contain game data (gamedata) if successful.
	Status changes to 'ingame' on success."""
	if len(cmd) != 3:
		sendError(client, 'Invalid game name')
		return
	else:
		gamename = cmd[2]

	if client.name == None:
		if sendMsg:
			sendError(client, 'You must be logged in to join a game')
	elif client.gamekey != None:
		if sendMsg:
			sendError(client, 'You are already in a game')
	elif gamename not in client.factory.games.keys():
		if sendMsg:
			sendError(client, 'There is currently no game with that name')
	elif (len(client.factory.games[gamename]['players'])
			== int(client.factory.games[gamename]['playerlimit'])):
		if sendMsg:
			sendError(client, 'That game is full')
	else:
		servercommands.joinGame(client, gamename)
		# Log
		logMsg('Join game successful: "'+client.name
				+'"added to "'+gamename+'"')
		if sendMsg:
			sendToGame(client, gamename,
						{'message':client.name+' joined the game'})
			sendToLobby(client, {})

def quitGame(client, sendMsg=True):
	"""Attempt to quit game.
	Response will contain error message (err) if failed.
	Response will contain lobby data (games) if successful.
	Status changes to 'inlobby' on success."""
	if client.gamekey == None:
		if sendMsg:
			sendError(client, 'You are not in a game yet')
	else:
		# Capture game name
		gamename = client.gamekey

		servercommands.quitGame(client)
		# Log
		logMsg('Quit game successful: "'+client.name
				+'" removed from "'+gamename+'"')
		if sendMsg:
			sendToGame(client, gamename, 
				{'message':client.name+' left the game'})
			sendToLobby(client, {})

def levelup(client, cmd, sendMsg=True):
	"""Attempt to level up player.
	Response will contain error message (err) if failed.
	Response will contain lobby data (games) if successful.
	Status changes to 'inlobby' on success."""
	if len(cmd) != 2:
		sendError(client, 'Invalid stat name')
		return
	else:
		statname = cmd[1]

	if client.playerdata == None:
		if sendMsg:
			sendError(client, 'You must be logged in to level up')
	elif statname not in client.playerdata['stats'].keys():
		if sendMsg:
			sendError(client, "Couldn't find that stat, try again")
	elif client.playerdata['exp'] <= 0:
		if sendMsg:
			sendError(client, "You don't have enough XP, win some games first")
	else:
		servercommands.levelUp(client, statname)
		# Log
		logMsg('Level up successful: "'+statname
				+'" increased by 1 for "'+client.name+'"')
		if sendMsg:
			sendResp(client, {'message':statname+' increased by 1'})

def logout(client, sendMsg=True):
	"""Attempt to log client out.
	Response will contain error message (err) if failed.
	Response will contain if status of 'logged_out' successful.
	Status changes to 'logging_in' on success."""
	# Clear game data
	quitGame(client, False)

	if client.name == None:
		if sendMsg:
			sendError(client, "You haven't logged in yet")
	else:
		# Capture username
		username = client.name

		servercommands.logout(client)
		# Log
		logMsg('Logout successful: "'+username+'" logged out')
		if sendMsg:
			sendResp(client, {'status':'Logging in',
							'message':'Logged out'})

def closeConn(client):
	"""Remove client data and close connection with client"""
	logMsg('Closing client connection')
	# Clear client data
	logout(client, False)
	client.factory.clients.remove(client)
	# Disconnect
	client.abortConnection()
