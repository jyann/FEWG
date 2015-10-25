from serverfuncts import addStatusInfo
import gamecommands

def executeGameFunct(client, gameFunct, targetkey):
	"""Attempt to execute specified game function.
	Response will contain error response if failed.
	Response will contain lobby data (games) if successful.
	Status does not change on success."""
	if client.gamekey == None:
		# Send response to client
		resp = {}
		resp['err'] = 'You are not in a game'
		addStatusInfo(client, resp)
		client.sendMessage(client.factory.json_encoder.encode(resp))
	elif targetkey not in client.factory.games[client.gamekey]['players'].keys():
		# Send response to client
		resp = {}
		resp['err'] = "Couldn't find that player in this game"
		addStatusInfo(client, resp)
		client.sendMessage(client.factory.json_encoder.encode(resp))
	elif client.name in client.factory.games[client.gamekey]['graveyard']:
		# Send response to client
		resp = {}
		resp['err'] = "You can't do that from the graveyard"
		addStatusInfo(client, resp)
		client.sendMessage(client.factory.json_encoder.encode(resp))
	else:
		gameFunct(client.factory.games[client.gamekey], client.name, targetkey)
		# Send response to specified clients
		clientlist = client.factory.games[client.gamekey]['players'].keys()
		resp = {}
		resp['gamedata'] = client.factory.games[client.gamekey]
		client.factory.sendToClients(clientlist, client.factory.json_encoder.encode(resp))

def attack(client, targetkey):
	"""Attempt to attack.
	Calls executeGameFunct."""
	executeGameFunct(client, gamecommands.attack, targetkey)

def defend(client, targetkey):
	"""Attempt to defend.
	Calls executeGameFunct."""
	executeGameFunct(client, gamecommands.defend, targetkey)
