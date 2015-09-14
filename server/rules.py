def log(msg):
	print msg

def login(username, password, client):
	if username in self.factory.names:
		log('login failed')
		log('names: '+str(client.factory.names))

		return client, 'failed\n'
	else:
		client.name = username
		client.factory.names.append(username)

		log(name+' logged in')
		log('names: '+str(client.factory.names))

		return client, 'success\n'

def newGame():
	game = {}
	game['players'] = {}
	return game

def createGame(gamename, client):
	if gamename not in client.factory.games.keys():
		client.factory.games[gamename] = newGame()

		log('game '+gamename+' created')
		log('games: '+str(client.factory.games))

		return client, 'sucess\n'
	else:
		log('game '+gamename+' not created')
		log('games: '+str(client.factory.games))

		return client, 'failed\n'

def joinGame(gamename, playerdata, client):
	cond1 = gamename in client.factory.games.keys()
	cond2 = client.name not in client.factory.games[gamename]['players']
	if cond1 and cond2:
		client.gamekey = gamename
		client.factory.games[gamename]['players'][client.name] = playerdata

		log(client.name+' added to game '+client.gamekey)
		log('games: '+str(client.factory.games))

		return client, 'success\n'
	else:
		log(client.name+' not added to game '+gamename)
		log('client.gamekey='+str(client.gamekey))
		log('games: '+str(client.factory.games))

		return client, 'failed\n'
