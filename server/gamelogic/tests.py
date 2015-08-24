import unittest

from gamelogic.game import Game

class WaitingRules(unittest.TestCase):
	testnames = ['dualGameWaiting']

	def dualGameWaiting(self):
		g = Game()

		g.processCommand('player1','add')
		self.assertEqual(g.state, 'waiting')
		self.assertEqual(g.winner, None)
		self.assertTrue('player1' in g.players.keys())
		self.assertEqual(g.players['player1'].status, 'waiting')
		self.assertEqual(g.graveyard, [])
