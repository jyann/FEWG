CODES = {'success':'success\n', 'failed':'failed\n', 'shutdown':'shutdown\n'}

def logMsg(msg):
	print msg

def login(username, password, client):
	cond1 = username in client.factory.named_clients.keys()
	cond2 = client.name in client.factory.named_clients.keys()
	if cond1 or cond2:
		client.transport.write(CODES['failed'])
		return client

	else:
		client.name = username
		client.factory.named_clients[username] = client

		client.transport.write(CODES['success'])
		return client

def newGame():
	game = {}
	game['players'] = {}
	return game

def createGame(gamename, client):
	if client.factory.redis_conn.setnx(gamename, newGame()):
		client.factory.games.append(gamename)
		client.factory.sendToAll(CODES['success'])
		return client

	else:
		client.transport.write(CODES['failed'])
		return client

def joinGame(gamename, playerdata, client):
	cond1 = client.name != None
	cond2 = client.gamekey == None
	cond3 = gamename in client.factory.games
	if cond1 and cond2 and cond3:
		client.gamekey = gamename

		rl = client.factory.redis_lock.lock(gamename, 1000) # lock game
		gamestr = client.factory.redis_conn.get(gamename) # get game
		game = self.factory.json_decoder(gamestr) # string to dict
		if client.name not in game['players'].keys():
			game['players'][client.name] = playerdata # add player
			gamestr = self.factory.json_encoder(game) # dict to string
			client.factory.redis_conn.set(gamename, gamestr) # push change
		client.factory.redis_lock.unlock(rl) # unlock game
		
		client.factory.sendToClients(game['players'].keys(), CODES['success'])
		return client

	else:
		client.transport.write(CODES['failed'])
		return client

def quitGame(client):
	cond1 = client.gamekey != None
	if cond1:
		gamename = client.gamekey

		rl = client.factory.redis_lock.lock(gamename, 1000) # lock game
		gamestr = client.factory.redis_conn.get(gamename) # get game
		game = self.factory.json_decoder(gamestr) # string to dict
		players = game['players'].keys() # players to send message to
		del game['players'][client.name] # remove player
		gamestr = self.factory.json_encoder(game) # dict to string
		client.factory.redis_conn.set(gamename, gamestr) # push change
		client.factory.redis_lock.unlock(rl) # unlock game

		client.gamekey = None

		client.sendToClients(players, CODES['success'])
		return client

	else:
		client.transport.write(CODES['failed'])
		return client

def logout(client):
	client = quitGame(client)

	cond1 = client.name != None
	if cond1:
		del client.factory.named_clients[client.name]
		client.name = None

		client.transport.write(CODES['success'])
		return client

	else:
		client.transport.write(CODES['failed'])
		return client

def onCloseConn(client):
	client = logout(client)
	client.transport.write(CODES['shutdown'])
	client.factory.clients.remove(client)

	return client
