from serverfuncts import sendResp, sendError, sendToLobby, sendToGame, quitGame, gamesList
import gamecommands

def endGame(client, gamename):
	for v in client.factory.named_clients.values():
		if v.gamekey == gamename:
			quitGame(v, False)
	del client.factory.games[gamename]

def executeGameFunct(client, gameFunct, targetkey):
	"""Attempt to execute specified game function.
	Response will contain error response if failed.
	Response will contain lobby data (games) if successful.
	Status does not change on success."""
	if client.gamekey == None:
		sendError(client, 'You are not in a game')
	elif (len(client.factory.games[client.gamekey]['players']) 
			!= client.factory.games[client.gamekey]['playerlimit']):
		sendError(client, 'The game is not ready yet')
	elif targetkey not in client.factory.games[client.gamekey]['players'].keys():
		sendError(client, "Couldn't find that player in this game")
	elif client.name in client.factory.games[client.gamekey]['graveyard']:
		sendError(client, "You can't do that from the graveyard")
	else:
		gameFunct(client.factory.games[client.gamekey], client.name, targetkey)

	if client.factory.games[client.gamekey]['winner'] == 'NONE':
		sendToGame(client, client.gamekey, {'status':'In game'})
	else:
		sendToGame(client, client.gamekey,
				{'winner':client.factory.games[client.gamekey]['winner']})
		endGame(client, client.gamekey)
		sendToLobby(client, {})

def attack(client, cmd):
	"""Attempt to attack.
	Calls executeGameFunct."""
	if len(cmd) != 2:
		sendError(client, 'Invalid target')
		return
	else:
		targetkey = cmd[1]

	executeGameFunct(client, gamecommands.attack, targetkey)

def defend(client, cmd):
	"""Attempt to defend.
	Calls executeGameFunct."""
	if len(cmd) != 2:
		sendError(client, 'Invalid target')
		return
	else:
		targetkey = cmd[1]

	executeGameFunct(client, gamecommands.defend, targetkey)

