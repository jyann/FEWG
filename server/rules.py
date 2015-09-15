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
	if gamename not in client.factory.games.keys():
		client.factory.games[gamename] = newGame()

		client.factory.sendToAll(CODES['success'])

		return client

	else:
		logMsg('games='+str(client.factory.games))

		client.transport.write(CODES['failed'])

		return client

def joinGame(gamename, playerdata, client):
	cond1 = client.name != None
	cond2 = client.gamekey == None
	cond3 = gamename in client.factory.games.keys()
	cond4 = client.name not in client.factory.games[gamename]['players']
	if cond1 and cond2 and cond3 and cond4:
		client.gamekey = gamename
		client.factory.games[gamename]['players'][client.name] = playerdata

		client.sendToGame(CODES['success'])

		return client

	else:
		client.transport.write(CODES['failed'])

		return client

def quitGame(client):
	cond1 = client.gamekey != None
	if cond1:
		client.sendToGame(CODES['success'])

		del client.factory.games[client.gamekey]['players'][client.name]
		client.gamekey = None

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
