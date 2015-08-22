from players import *

valid_commands = ['attack','defend','focus','dodge']

def subtract(value, varflow, player, target):
	curval = value
	for varkey in varflow:
		if target.vars[varkey]-curval < 0:
			curval -= target.vars[varkey]
			target.vars[varkey] = 0
		else:
			target.vars[varkey] -= curval
			break

	return player, target

def extract_players(game, playerkey, targetkey):
	return game.players[playerkey], game.players[targetkey]

def replace_players(game, playerkey, player, targetkey, target):
	game.players[playerkey] = player
	game.players[targetkey] = target
	return game

def check_end_game(game):
	if len(game.players)-len(game.graveyard) == 1:
		game.winner = list(set(game.players.keys())-set(game.graveyard))[0]
		game.state = 'finished'
	elif len(game.players) == len(game.graveyard):
		game.winner = 'draw'
		game.state = 'finished'

# Command functions:

def attack(game, playerkey, targetkey):
	player,target = extract_players(game, playerkey, targetkey)

	if player.vars['accuracy'] >= target.vars['agility']:
		player, target = subtract(player.stats['attack'],['defense','health'],player,target)

	player.reset_vars(['accuracy'])
	target.reset_vars(['agility'])

	if target.vars['health'] <= 0:
		game.graveyard.append(targetkey)

	game = check_end_game(game)

	return replace_players(game,playerkey,player,targetkey,target)

def defend(game, playerkey, targetkey):
	player,target = extract_players(game, playerkey, targetkey)

	player.vars['defense'] += target.stats['defense']

	return replace_players(game,playerkey,player,targetkey,target)
