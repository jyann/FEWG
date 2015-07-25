import game_rules
import waiting_room_rules

class Game(object):
	states = ['waiting', 'running']

	valid_universal_commands = ['quit']

	def __init__(self, player_limit=2):
		self.winner = None
		self.state = 'waiting'

		self.command_functs = {}
		# init waiting room rules
		self.command_functs['waiting'] = {}
		for cmd_key in waiting_room_rules.valid_commands:
			self.command_functs['waiting'][cmd_key] = getattr(waiting_room_rules, cmd_key)
		# init game rules
		self.command_functs['running'] = {}
		for cmd_key in game_rules.valid_commands:
			self.command_functs['running'][cmd_key] = getattr(game_rules, cmd_key)

		self.player_limit = player_limit
		self.players = {}
		self.ready_flags = {}

	def processCommand(self, name, command):
		try:
			if command == 'quit':
				self.quit(name)
			else:
				cmd = command.split(' ')
				if len(cmd) == 1:
					self = self.command_functs[self.state][cmd[0]](self, name)
				else:
					a, d = self.players[name], self.players[cmd[1]]
					self.players[name], self.players[cmd[1]] = self.command_functs[self.state][cmd[0]](a, d)
		except Exception as e:
			print str(e)

	def quit(self, name):
		del self.players[name]
		self.reset()
		self.state = 'waiting'

	def reset(self):
		for player in self.players.values():
			player.reset_stats()
