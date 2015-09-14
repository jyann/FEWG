CODES = {'success':'success\n', 'failed':'failed\n', 'shutdown':'shutdown\n'}

def logMsg(msg):
	print msg

def login(username, password, client):
	cond1 = username in client.factory.named_clients.keys()
	cond2 = client.name in client.factory.named_clients.keys()
	if cond1 or cond2:
		logMsg('login failed')
		logMsg('names: '+str(client.factory.named_clients.keys()))

		return client, CODES['failed']
	else:
		client.name = username
		client.factory.named_clients[username] = client

		logMsg(client.name+' logged in')
		logMsg('names: '+str(client.factory.named_clients.keys()))

		return client, CODES['success']

def newGame():
	game = {}
	game['players'] = {}
	return game

def createGame(gamename, client):
	if gamename not in client.factory.games.keys():
		client.factory.games[gamename] = newGame()

		logMsg('game '+gamename+' created')
		logMsg('games: '+str(client.factory.games))

		return client, CODES['success']
	else:
		logMsg('game '+gamename+' not created')
		logMsg('games: '+str(client.factory.games))

		return client, CODES['failed']

def joinGame(gamename, playerdata, client):
	cond1 = client.name != None
	cond2 = client.gamekey == None
	cond3 = gamename in client.factory.games.keys()
	cond4 = client.name not in client.factory.games[gamename]['players']
	if cond1 and cond2 and cond3 and cond4:
		client.gamekey = gamename
		client.factory.games[gamename]['players'][client.name] = playerdata

		logMsg(client.name+' added to game '+client.gamekey)
		logMsg('games: '+str(client.factory.games))

		return client, CODES['success']
	else:
		logMsg('player not added to game '+gamename)
		logMsg('client.gamekey='+str(client.gamekey))
		logMsg('games: '+str(client.factory.games))

		return client, CODES['failed']

def quitGame(client):
	cond1 = client.gamekey != None
	if cond1:
		logMsg(client.name+' removed from game '+client.gamekey)
		logMsg('games: '+str(client.factory.games))

		del client.factory.games[client.gamekey]['players'][client.name]
		client.gamekey = None

		return client, CODES['success']
	else:
		logMsg('player not added to game '+gamename)
		logMsg('client.gamekey='+str(client.gamekey))
		logMsg('games: '+str(client.factory.games))

		return client, CODES['failed']

def logout(client):
	quitGame(client)

	cond1 = client.name != None
	if cond1:
		logMsg(client.name+' logged in')
		logMsg('names: '+str(client.factory.named_clients.keys()))

		del client.factory.named_clients[client.name]
		client.name = None

		return client, CODES['success']
	else:
		logMsg('login failed')
		logMsg('names: '+str(client.factory.named_clients.keys()))

		return client, CODES['failed']

def onCloseConn(client):
	client, msg = logout(client)

	client.factory.clients.remove(client)

	return client, CODES['shutdown']
