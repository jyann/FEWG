from serverfuncts import addStatusInfo
from gamelogic import game_rules

def executeGameFunct(client, gameFunct, targetkey):
	if client.gamekey == None:
		resp = {}
		resp['err'] = 'You are not in a game'
		addStatusInfo(client, resp)
		client.sendMessage(client.factory.json_encoder.encode(resp))
	elif targetkey not in client.factory.games[client.gamekey]['players'].keys():
		resp = {}
		addStatusInfo(client, resp)
		client.sendMessage(client.factory.json_encoder.encode(resp))
	elif client.name in client.factory.games[client.gamekey]['graveyard']:
		resp = {}
		addStatusInfo(client, resp)
		client.sendMessage(client.factory.json_encoder.encode(resp))
	else:
		gameFunct(client.factory.games[client.gamekey], client.name, targetkey)
		
		clientlist = client.factory.games[client.gamekey]['players'].keys()
		
		resp = {}
		resp['gamedata'] = client.factory.games[client.gamekey]
		client.factory.sendToClients(clientlist, client.factory.json_encoder.encode(resp))

def attack(client, targetkey):
	executeGameFunct(client, game_rules.attack, targetkey)

def defend(client, targetkey):
	executeGameFunct(client, game_rules.defend, targetkey)
