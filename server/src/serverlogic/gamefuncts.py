from serverfuncts import sendGameMsg
from gamelogic import game_rules

def executeGameFunct(client, gameFunct, targetkey):
	if client.gamekey == None:
		resp = {}
		resp['err'] = 'You are not in a game'
		client.sendMessage(client.json_encoder.encode(resp))
	elif targetkey not in client.factory.games[client.gamekey]['players'].keys():
		pass
	elif client.name in client.factory.games[client.gamekey]['graveyard']:
		pass
	else:
		gameFunct(client.factory.games[client.gamekey], client.name, targetkey)
		sendGameMsg(client)

def attack(client, targetkey):
	executeGameFunct(client, game_rules.attack, targetkey)

def defend(client, targetkey):
	executeGameFunct(client, game_rules.defend, targetkey)
