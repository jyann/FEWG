from serverfuncts import sendResp, sendToGame
import gamecommands

def executeGameFunct(client, gameFunct, targetkey):
	"""Attempt to execute specified game function.
	Response will contain error response if failed.
	Response will contain lobby data (games) if successful.
	Status does not change on success."""
	if client.gamekey == None:
		sendResp(client, {'err':'You are not in a game'})
	elif targetkey not in client.factory.games[client.gamekey]['players'].keys():
		sendResp(client, {'err':"Couldn't find that player in this game"})
	elif client.name in client.factory.games[client.gamekey]['graveyard']:
		sendResp(client, {'err':"You can't do that from the graveyard"})
	else:
		gameFunct(client.factory.games[client.gamekey], client.name, targetkey)

		sendToGame(client, client.gamekey, {'gamedata':client.factory.games[client.gamekey]})

def attack(client, targetkey):
	"""Attempt to attack.
	Calls executeGameFunct."""
	executeGameFunct(client, gamecommands.attack, targetkey)

def defend(client, targetkey):
	"""Attempt to defend.
	Calls executeGameFunct."""
	executeGameFunct(client, gamecommands.defend, targetkey)
