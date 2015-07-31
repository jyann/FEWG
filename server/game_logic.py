import game_rules
import waiting_room_rules

class Game(object):
	states = ['waiting', 'running', 'finished']

	def __init__(self, player_llim=2, player_ulim=2):
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

		self.player_llim = player_llim
		self.player_ulim = player_ulim

		self.players = {}
		self.graveyard = []

	def processCommand(self, playerkey, command, targetkey=None):
		if targetkey == None:
			targetkey = playerkey

		try:
			if command == 'quit':
				self.quit(playerkey)
			else:
				self = self.command_functs[self.state][command](self, playerkey, targetkey)
		except Exception as e:
			return 'invalid command'

	def quit(self, playerkey):
		del self.players[playerkey]
		self.reset()
		self.state = 'waiting'

	def reset(self):
		for player in self.players.values():
			player.reset_vars()
		self.graveyard = []
		self.state = 'waiting'
