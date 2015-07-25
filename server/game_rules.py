from players import *

valid_commands = ['attack','defend','focus','dodge']

def subtract(value, statflow, attacker, defender):
	curval = value
	for stat in statflow:
		if defender.var_stats[stat]-curval < 0:
			curval -= defender.var_stats[stat]
			defender.var_stats[stat] = 0
		else:
			defender.var_stats[stat] -= curval
			break

	return attacker, defender

def reset_stats(statkeys, player):
	for stat in statkeys:
		player.var_stats[stat] = 0

def attack(attacker, defender):
	if attacker.var_stats['accuracy'] >= defender.var_stats['agility']:
		attacker, defender = subtract(attacker.perm_stats['attack'],['defense','health'],attacker,defender)

	attacker = reset_stats(['accuracy'], attacker)
	defender = reset_stats(['agility'], defender)

	return attacker, defender

def defend(attacker, defender):
	attacker.var_stats['defense'] += attacker.perm_stats['defense']
	return attacker, defender

def focus(attacker, defender):
	attacker.var_stats['accuracy'] += attacker.perm_stats['accuracy']
	return attacker, defender

def dodge(attacker, defender):
	attacker.var_stats['agility'] += attacker.perm_stats['agility']
	return attacker, defender
