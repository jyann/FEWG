CODES = {'success':'success\n', 'failed':'failed\n', 'shutdown':'shutdown\n'}
invalidNames = ['NONE']

def logMsg(msg):
	print msg

def sendGameMsg(client):
	clientlist = client.factory.games[client.gamekey]['players'].keys()
	msg = client.factory.json_encoder.encode(client.factory.games[client.gamekey])
	client.factory.sendToClients(clientlist, msg+'\n')

def login(client, username, password, sendMsg=True):
	# cond1: name not in use
	cond1 = username not in client.factory.named_clients.keys()
	# cond2: not already logged in
	cond2 = client.name not in client.factory.named_clients.keys()
	# cond3: name is valid
	cond3 = username not in invalidNames
	if cond1 and cond2 and cond3:
		client.name = username
		client.factory.named_clients[username] = client

		if sendMsg:
			msg = client.factory.json_encoder.encode(client.factory.games.keys())
			client.transport.write(msg+'\n')
	else:
		if sendMsg:
			client.transport.write(CODES['failed'])

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
			msg = client.factory.json_encoder.encode(client.factory.games.keys())
			client.factory.sendToClients(clientlist, msg+'\n')
	else:
		if sendMsg:
			client.transport.write(CODES['failed'])

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
			client.transport.write(CODES['failed'])

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

		client.gamekey = None

		if sendMsg:
			clientlist = client.factory.games[gamename]['players'].keys()
			msg = client.factory.json_encoder.encode(client.factory.games[gamename])
			client.factory.sendToClients(clientlist, msg+'\n')
			client.transport.write(CODES['success'])
	else:
		if sendMsg:
			client.transport.write(CODES['failed'])

def logout(client, sendMsg=True):
	quitGame(client, False)

	# cond1: client logged in
	cond1 = client.name != None
	if cond1:
		del client.factory.named_clients[client.name]
		client.name = None

		if sendMsg:
			client.transport.write(CODES['success'])
	else:
		if sendMsg:
			client.transport.write(CODES['failed'])

def onCloseConn(client, sendMsg=True):
	logout(client, False)
	if sendMsg:
		client.transport.write(CODES['shutdown'])
	client.factory.clients.remove(client)
