from serverfuncts import CODES, sendGameMsg
from gamelogic import game_rules

# universal condition 1: client in a game
def ucond1(client, targetkey):
	return client.gamekey != None
# universal condition 2: target in the same game
def ucond2(client, targetkey):
	return targetkey in client.factory.games[client.gamekey]['players'].keys()
# universal condition 3: client not dead
def ucond3(client, targetkey):
	return client.name not in client.factory.games[client.gamekey]['graveyard']

def attack(client, targetkey):
	cond1 = ucond1(client, targetkey)
	cond2 = ucond2(client, targetkey)
	cond3 = ucond3(client, targetkey)
	if cond1 and cond2 and cond3:
		game_rules.attack(client.factory.games[client.gamekey], client.name, targetkey)

		sendGameMsg(client)
	else:
		client.sendMessage(CODES['failed'])

def defend(client, targetkey):
	cond1 = ucond1(client, targetkey)
	cond2 = ucond2(client, targetkey)
	cond3 = ucond3(client, targetkey)
	if cond1 and cond2 and cond3:
		game_rules.defend(client.factory.games[client.gamekey], client.name, targetkey)

		sendGameMsg(client)
	else:
		client.sendMessage(CODES['failed'])
