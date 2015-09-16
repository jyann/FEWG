import unittest

from gamelogic.game import Game

class WaitingRules(unittest.TestCase):
	testnames = ['addPlayerTo2PlayerGame']

	def addPlayerTo2PlayerGame(self):
		g = Game(player_llim=2, player_ulim=2)

		g.processCommand('player1','add')
		self.assertEqual(g.state, 'waiting')
		self.assertEqual(g.winner, None)
		self.assertTrue('player1' in g.players.keys())
		self.assertEqual(g.players['player1'].status, 'waiting')
		self.assertEqual(g.graveyard, [])
