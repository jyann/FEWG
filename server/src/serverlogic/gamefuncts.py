from serverfuncts import sendResp, sendToLobby, sendToGame, quitGame, gamesList
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
		sendResp(client, {'err':'You are not in a game'})
	elif len(client.factory.games[client.gamekey]['players']) != client.factory.games[client.gamekey]['playerlimit']:
		sendResp(client, {'err':'The game is not ready yet'})
	elif targetkey not in client.factory.games[client.gamekey]['players'].keys():
		sendResp(client, {'err':"Couldn't find that player in this game"})
	elif client.name in client.factory.games[client.gamekey]['graveyard']:
		sendResp(client, {'err':"You can't do that from the graveyard"})
	else:
		gameFunct(client.factory.games[client.gamekey], client.name, targetkey)

	if client.factory.games[client.gamekey]['winner'] == 'NONE':
		sendToGame(client, client.gamekey, {'status':'In game'})
	else:
		sendToGame(client, client.gamekey,
				{'winner':client.factory.games[client.gamekey]['winner']})
		endGame(client, client.gamekey)
		sendToLobby(client, {})

def attack(client, targetkey):
	"""Attempt to attack.
	Calls executeGameFunct."""
	executeGameFunct(client, gamecommands.attack, targetkey)

def defend(client, targetkey):
	"""Attempt to defend.
	Calls executeGameFunct."""
	executeGameFunct(client, gamecommands.defend, targetkey)
