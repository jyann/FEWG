def logMsg(msg):
	print msg

def login(username, password, client):
	if username in client.factory.names or client.name in client.factory.names:
		logMsg('login failed')
		logMsg('names: '+str(client.factory.names))

		return client, 'failed\n'
	else:
		client.name = username
		client.factory.names.append(username)

		logMsg(client.name+' logged in')
		logMsg('names: '+str(client.factory.names))

		return client, 'success\n'

def newGame():
	game = {}
	game['players'] = {}
	return game

def createGame(gamename, client):
	if gamename not in client.factory.games.keys():
		client.factory.games[gamename] = newGame()

		logMsg('game '+gamename+' created')
		logMsg('games: '+str(client.factory.games))

		return client, 'sucess\n'
	else:
		logMsg('game '+gamename+' not created')
		logMsg('games: '+str(client.factory.games))

		return client, 'failed\n'

def joinGame(gamename, playerdata, client):
	cond1 = gamename in client.factory.games.keys()
	cond2 = client.name not in client.factory.games[gamename]['players']
	if cond1 and cond2:
		client.gamekey = gamename
		client.factory.games[gamename]['players'][client.name] = playerdata

		logMsg(client.name+' added to game '+client.gamekey)
		logMsg('games: '+str(client.factory.games))

		return client, 'success\n'
	else:
		logMsg(client.name+' not added to game '+gamename)
		logMsg('client.gamekey='+str(client.gamekey))
		logMsg('games: '+str(client.factory.games))

		return client, 'failed\n'
