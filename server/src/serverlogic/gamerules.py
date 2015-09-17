from rules import CODES
from gamelogic import game_rules

def attack(client, targetkey):
	# cond1: client in a game
	cond1 = client.gamekey != None
	# cond2: target in the same game
	cond2 = targetkey in client.factory.games[client.gamekey]['players'].keys()
	# cond3: client not dead
	cond3 = client.name not in client.factory.games[client.gamekey]['graveyard']
	if cond1 and cond2 and cond3:
		game_rules.attack(client.factory.games[client.gamekey], client.name, targetkey)

		clientlist = client.factory.games[client.gamekey]['players'].keys()
		msg = client.factory.json_encoder.encode(client.factory.games[client.gamekey])
		client.factory.sendToClients(clientlist, msg)
	else:
		client.transport.write(CODES['failed'])


	return client
