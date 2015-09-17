CODES = {'success':'success\n', 'failed':'failed\n', 'shutdown':'shutdown\n'}
invalidNames = ['NONE']

def logMsg(msg):
	print msg

def login(username, password, client, sendMsg=True):
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
		return client
	else:
		if sendMsg:
			client.transport.write(CODES['failed'])
		return client

def newGame():
	game = {}
	game['players'] = {}
	game['graveyard'] = []
	game['winner'] = 'NONE'
	return game

def createGame(gamename, client, sendMsg=True):
	#if client.factory.redis_conn.setnx(gamename, newGame()):

	cond1 = gamename not in client.factory.games.keys()
	cond2 = client.name != None
	if cond1 and cond2:
		client.factory.games[gamename] = newGame()

		if sendMsg:
			clientlist = client.factory.named_clients.keys()
			msg = client.factory.json_encoder.encode(client.factory.games.keys())
			client.factory.sendToClients(clientlist, msg+'\n')
		return client

	else:
		if sendMsg:
			client.transport.write(CODES['failed'])
		return client

def joinGame(gamename, playerdata, client, sendMsg=True):
	cond1 = client.name != None
	cond2 = client.gamekey == None
	cond3 = gamename in client.factory.games.keys()
	cond4 = client.name not in client.factory.games[gamename]['players'].keys()
	if cond1 and cond2 and cond3 and cond4:
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
			clientlist = client.factory.games[gamename]['players'].keys()
			msg = client.factory.json_encoder.encode(client.factory.games[gamename])
			client.factory.sendToClients(clientlist, msg+'\n')
		return client

	else:
		if sendMsg:
			client.transport.write(CODES['failed'])
		return client

def quitGame(client, sendMsg=True):
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

		return client

	else:
		if sendMsg:
			client.transport.write(CODES['failed'])
		return client

def logout(client, sendMsg=True):
	client = quitGame(client, False)

	cond1 = client.name != None
	if cond1:
		del client.factory.named_clients[client.name]
		client.name = None

		if sendMsg:
			client.transport.write(CODES['success'])
		return client

	else:
		if sendMsg:
			client.transport.write(CODES['failed'])
		return client

def onCloseConn(client, sendMsg=True):
	client = logout(client)
	if sendMsg:
		client.transport.write(CODES['shutdown'])
	client.factory.clients.remove(client)

	return client
