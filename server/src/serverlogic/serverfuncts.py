from storage import getPlayer

CODES = {'success':'success', 'failed':'failed', 'close connection':'shutdown'}
invalidNames = ['NONE']

def logMsg(msg):
	print msg

def resetPlayer(player):
	player['vars']['health'] = player['stats']['health']
	player['vars']['defense'] = 0

def sendGameMsg(client):
	clientlist = client.factory.games[client.gamekey]['players'].keys()
	msg = client.factory.json_encoder.encode({'game':client.factory.games[client.gamekey]})
	client.factory.sendToClients(clientlist, msg)

def gamesList(client):
	return client.factory.json_encoder.encode({'gameslist':client.factory.games.keys()})

def login(client, username, password, sendMsg=True):
	# cond1: name not in use
	cond1 = username not in client.factory.named_clients.keys()
	# cond2: not already logged in
	cond2 = client.name not in client.factory.named_clients.keys()
	# cond3: name is valid
	cond3 = username not in invalidNames
	if cond1 and cond2 and cond3:
		client.name = username
		client.playerdata = getPlayer(username)
		
		client.factory.named_clients[username] = client

		if sendMsg:
			client.sendMessage(gamesList(client))
	else:
		if sendMsg:
			client.sendMessage(CODES['failed'])

def newGame():
	game = {}
	game['players'] = {}
	game['graveyard'] = []
	game['winner'] = 'NONE'
	return game

def createGame(client, gamename, sendMsg=True):
	#if client.factory.redis_conn.setnx(gamename, newGame()):

	# cond1: game doesn't already exist
	cond1 = gamename not in client.factory.games.keys()
	# cond2: client logged in
	cond2 = client.name != None
	if cond1 and cond2:
		client.factory.games[gamename] = newGame()

		if sendMsg:
			clientlist = client.factory.named_clients.keys()
			msg = gamesList(client)
			client.factory.sendToClients(clientlist, msg)
	else:
		if sendMsg:
			client.sendMessage(CODES['failed'])

def joinGame(client, gamename, playerdata, sendMsg=True):
	# cond1: client logged in
	cond1 = client.name != None
	# cond2: client not already in a game
	cond2 = client.gamekey == None
	# cond3: game exists
	cond3 = gamename in client.factory.games.keys()
	if cond1 and cond2 and cond3:
		client.gamekey = gamename

		#rl = client.factory.redis_lock.lock(gamename, 1000) # lock game
		#gamestr = client.factory.redis_conn.get(gamename) # get game
		#game = self.factory.json_decoder(gamestr) # string to dict
		#if client.name not in game['players'].keys():
		#	game['players'][client.name] = playerdata # add player
		#	gamestr = self.factory.json_encoder(game) # dict to string
		#	client.factory.redis_conn.set(gamename, gamestr) # push change
		#client.factory.redis_lock.unlock(rl) # unlock game

		client.factory.games[gamename]['players'][client.name] = playerdata
		
		if sendMsg:
			sendGameMsg(client)
	else:
		if sendMsg:
			client.sendMessage(CODES['failed'])

def quitGame(client, sendMsg=True):
	# cond1: client in a game
	cond1 = client.gamekey != None
	if cond1:
		gamename = client.gamekey

		#rl = client.factory.redis_lock.lock(gamename, 1000) # lock game
		#gamestr = client.factory.redis_conn.get(gamename) # get game
		#game = self.factory.json_decoder(gamestr) # string to dict
		#players = game['players'].keys() # players to send message to
		#del game['players'][client.name] # remove player
		#gamestr = self.factory.json_encoder(game) # dict to string
		#client.factory.redis_conn.set(gamename, gamestr) # push change
		#client.factory.redis_lock.unlock(rl) # unlock game

		del client.factory.games[gamename]['players'][client.name]
		if client.name in client.factory.games[gamename]['graveyard']:
			client.factory.games[gamename]['graveyard'].remove(client.name)
		if client.factory.games[gamename]['winner'] == client.name:
			client.factory.games[gamename]['winner'] = 'NONE'
		resetPlayer(client.playerdata)
		client.gamekey = None

		if sendMsg:
			clientlist = client.factory.games[gamename]['players'].keys()
			msg = client.factory.json_encoder.encode(client.factory.games[gamename])
			client.factory.sendToClients(clientlist, msg)
			client.sendMessage(gamesList(client))
	else:
		if sendMsg:
			client.sendMessage(CODES['failed'])

def levelup(client, statname):
	cond1 = client.playerdata != None
	cond2 = statname in client.playerdata['stats'].keys()
	cond3 = client.playerdata['exp'] > 0
	if cond1 and cond2 and cond3:
		client.playerdata['stats'][statname] += 1
		client.playerdata['exp'] -= 1

		client.sendMessage(CODES['success'])
	else:
		client.sendMessage(CODES['failed'])

def logout(client, sendMsg=True):
	quitGame(client, False)

	# cond1: client logged in
	cond1 = client.name != None
	if cond1:
		del client.factory.named_clients[client.name]
		client.name = None

		if sendMsg:
			client.sendMessage('logged out')
	else:
		if sendMsg:
			client.sendMessage(CODES['failed'])

def onCloseConn(client, sendMsg=True):
	logout(client, False)
	if sendMsg:
		client.sendMessage('confirm with code:'+CODES['close connection'])
	client.factory.clients.remove(client)
