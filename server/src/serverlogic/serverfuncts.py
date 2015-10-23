import logging

from storage import getPlayer

logging.basicConfig(level=logging.DEBUG, filename='server.log', format='%(asctime)s | %(message)s')

invalidNames = ['NONE']

def logMsg(msg):
	print msg
	logging.info(msg)

def resetPlayer(player):
	player['vars']['health'] = player['stats']['health']
	player['vars']['defense'] = 0

def gamesList(client):
	return [{'name':k,'player_count':len(v['players'])} for k, v in client.factory.games.items()]

def addStatusInfo(client, resp):
	if client.status == 'inlobby':
		resp['games'] = gamesList(client)
	elif client.status == 'ingame':
		resp['gamedata'] = client.factory.games[client.gamekey]

def login(client, username, password, sendMsg=True):
	if client.status != 'logging_in':
		logMsg('Login failed: status != logging_in')
		if sendMsg:
			resp = {}
			resp['err'] = 'You are already logged in'
			addStatusInfo(client, resp)

			logMsg('to: '+str(client.name)+' - '+str(resp))
			client.sendMessage(client.factory.json_encoder.encode(resp))
	elif client.name in client.factory.named_clients.keys():
		if sendMsg:
			resp = {}
			resp['err'] = 'You are already logged in'

			logMsg('to: '+str(client.name)+' - '+str(resp))
			client.sendMessage(client.factory.json_encoder.encode(resp))
	elif username in client.factory.named_clients.keys():
		if sendMsg:
			resp = {}
			resp['err'] = 'That username is already in use'

			logMsg('to: '+str(client.name)+' - '+str(resp))
			client.sendMessage(client.factory.json_encoder.encode(resp))
	elif username in invalidNames:
		if sendMsg:
			resp = {}
			resp['err'] = 'That username is not valid, try again'

			logMsg('to: '+str(client.name)+' - '+str(resp))
			client.sendMessage(client.factory.json_encoder.encode(resp))
	else:
		client.status = 'inlobby'
		client.name = username
		client.playerdata = getPlayer(username)
		client.factory.named_clients[username] = client

		if sendMsg:
			resp = {}
			addStatusInfo(client, resp)

			logMsg('to: '+str(client.name)+' - '+str(resp))
			client.sendMessage(client.factory.json_encoder.encode(resp))

def newGame(attr):
	game = {}
	game['players'] = {}
	game['graveyard'] = []
	game['winner'] = 'NONE'
	return game

def createGame(client, gamename, sendMsg=True):
	if client.name == None:
		if sendMsg:
			resp = {}
			resp['err'] = 'You must be logged in to create a game'
			addStatusInfo(client, resp)

			logMsg('to: '+str(client.name)+' - '+str(resp))
			client.sendMessage(client.factory.json_encoder.encode(resp))
	elif client.status != 'inlobby':
		if sendMsg:
			resp = {}
			resp['err'] = 'Must be in lobby to create a game'
			addStatusInfo(client, resp)

			logMsg('to: '+str(client.name)+' - '+str(resp))
			client.sendMessage(client.factory.json_encoder.encode(resp))
	elif gamename in client.factory.games.keys():
		if sendMsg:
			resp = {}
			resp['err'] = 'That game already exists'
			addStatusInfo(client, resp)

			logMsg('to: '+str(client.name)+' - '+str(resp))
			client.sendMessage(client.factory.json_encoder.encode(resp))
	elif len(client.factory.games) == client.factory.game_limit:
		if sendMsg:
			resp = {}
			resp['err'] = 'Game limit reached, try again later or join another game'
			addStatusInfo(client, resp)

			logMsg('to: '+str(client.name)+' - '+str(resp))
			client.sendMessage(client.factory.json_encoder.encode(resp))
	else:
		# no problems detected, create the game
		client.factory.games[gamename] = newGame(None)

		if sendMsg:
			clientlist = [k for k, v in client.factory.named_clients.items() if v.gamekey == None]

			resp = {}
			addStatusInfo(client, resp)

			logMsg('to: '+str(clientlist)+' - '+str(resp))
			client.factory.sendToClients(clientlist, client.factory.json_encoder.encode(resp))
			

def joinGame(client, gamename, sendMsg=True):
	if client.name == None:
		if sendMsg:
			resp = {}
			resp['err'] = 'You must be logged in to join a game'
			addStatusInfo(client, resp)

			logMsg('to: '+str(client.name)+' - '+str(resp))
			client.sendMessage(client.factory.json_encoder.encode(resp))
	elif client.gamekey != None:
		if sendMsg:
			resp = {}
			resp['err'] = 'You are already in a game'
			addStatusInfo(client, resp)

			logMsg('to: '+str(client.name)+' - '+str(resp))
			client.sendMessage(client.factory.json_encoder.encode(resp))
	elif gamename not in client.factory.games.keys():
		if sendMsg:
			resp = {}
			resp['err'] = 'There is currently no game with that name'
			addStatusInfo(client, resp)

			logMsg('to: '+str(client.name)+' - '+str(resp))
			client.sendMessage(client.factory.json_encoder.encode(resp))
	else:
		client.status = 'ingame'
		client.gamekey = gamename

		client.factory.games[gamename]['players'][client.name] = client.playerdata

		if sendMsg:
			clientlist = client.factory.games[client.gamekey]['players'].keys()

			resp = {}
			addStatusInfo(client, resp)

			logMsg('to: '+str(client.name)+' - '+str(resp))
			client.factory.sendToClients(clientlist, client.factory.json_encoder.encode(resp))

def quitGame(client, sendMsg=True):
	if client.gamekey == None:
		if sendMsg:
			resp = {}
			resp['err'] = 'You are not in a game yet'
			addStatusInfo(client, resp)

			logMsg('to: '+str(client.name)+' - '+str(resp))
			client.sendMessage(client.factory.json_encoder.encode(resp))
	else:
		client.status = 'inlobby'
		gamename = client.gamekey

		del client.factory.games[gamename]['players'][client.name]
		if client.name in client.factory.games[gamename]['graveyard']:
			client.factory.games[gamename]['graveyard'].remove(client.name)
		if client.factory.games[gamename]['winner'] == client.name:
			client.factory.games[gamename]['winner'] = 'NONE'
		resetPlayer(client.playerdata)
		client.gamekey = None

		if sendMsg:
			clientlist = client.factory.games[gamename]['players'].keys()
			resp = {}
			resp['gamedata'] = client.factory.games[gamename]
			msg = client.factory.json_encoder.encode(resp)

			logMsg('to: '+str(clientlist)+' - '+str(resp))
			client.factory.sendToClients(clientlist, msg)

			resp = {}
			resp['games'] = gamesList(client)

			logMsg('to: '+str(client.name)+' - '+str(resp))
			client.sendMessage(client.factory.json_encoder.encode(resp))

def levelup(client, statname, sendMsg=True):
	if client.playerdata == None:
		if sendMsg:
			resp = {}
			resp['err'] = 'You must be logged in to level up'
			addStatusInfo(client, resp)

			logMsg('to: '+str(client.name)+' - '+str(resp))
			client.sendMessage(client.factory.json_encoder.encode(resp))
	if statname not in client.playerdata['stats'].keys():
		if sendMsg:
			resp = {}
			resp['err'] = "Couldn't fine that stat, try another again"
			addStatusInfo(client, resp)

			logMsg('to: '+str(client.name)+' - '+str(resp))
			client.sendMessage(client.factory.json_encoder.encode(resp))
	if client.playerdata['exp'] <= 0:
		if sendMsg:
			resp = {}
			resp['err'] = "You don't have enough XP, win some games first"
			addStatusInfo(client, resp)

			logMsg('to: '+str(client.name)+' - '+str(resp))
			client.sendMessage(client.factory.json_encoder.encode(resp))
	else:
		client.status = 'inlobby'
		client.playerdata['stats'][statname] += 1
		client.playerdata['exp'] -= 1

		if sendMsg:
			resp = {}
			resp['games'] = gamesList(client)

			logMsg('to: '+str(client.name)+' - '+str(resp))
			client.sendMessage(client.factory.json_encoder.encode(resp))

def logout(client, sendMsg=True):
	quitGame(client, False)

	if client.name == None:
		if sendMsg:
			resp = {}
			resp['err'] = "You haven't logged in yet"

			logMsg('to: '+str(client.name)+' - '+str(resp))
			client.sendMessage(client.factory.json_encoder.encode(resp))

	else:
		client.status = 'logging_in'
		del client.factory.named_clients[client.name]
		client.name = None

		if sendMsg:
			resp = {}
			resp['status'] = 'logged_out'

			logMsg('to: '+str(client.name)+' - '+str(resp))
			client.sendMessage(client.factory.json_encoder.encode(resp))

def onCloseConn(client):
	logout(client, False)

	client.factory.clients.remove(client)
	client.abortConnection()

def closeConn(self):
		logMsg('client closing')
		onCloseConn(self)
