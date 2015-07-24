import game_rules
import waiting_room_rules

class Player(object):
	def __init__(self):
		self.perm_stats = game_rules.perm_stat_defaults
		self.var_stats = game_rules.var_stat_defaults

	def reset_stats(self):
		for vskey in self.var_stats.keys():
			if game_rules.var_stats[vskey] == 0:
				self.var_stats[vskey] = 0
			else:
				self.var_stats[vskey] = self.perm_stats[vskey]

class Game(object):
	states = ['waiting', 'running']

	valid_universal_commands = ['quit']

	def __init__(self, player_limit=2):
		self.winner = None
		self.state = 'waiting'

		self.command_functs = {}
		# init waiting room rules
		self.command_functs['waiting'] = {}
		for cmd_key in waiting_room_rules.valid_waiting_room_commands:
			command_functs['waiting'][cmd_key] = getattr(waiting_room_rules, cmd_key)
		# init game rules
		self.command_functs['running'] = {}
		for cmd_key in game_rules.valid_commands:
			command_functs['running'][cmd_key] = getattr(game_rules, cmd_key)

		self.player_limit = player_limit
		self.players = {}
		self.ready_flags = {}

	def processCommand(self, name, cmd):
		if name in self.players.keys():
			if cmd == 'quit':
				self.quit(name)

	def quit(self, name):
		del self.players[name]
		self.reset()
		self.state = 'waiting'

	def reset(self):
		for player in self.players.values():
			player.reset_stats()
