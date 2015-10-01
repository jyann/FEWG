from serverlogic import storage, serverfuncts, gamefuncts

from time import sleep

from twisted.internet.protocol import ServerFactory
from TwistedWebsocket.server import Protocol
import re
#from redis import StrictRedis
#from redlock import Redlock
from json import JSONDecoder, JSONEncoder

class FEWGProtocol(Protocol):
	def onHandshake(self, header):
		g = re.search('Origin\s*:\s*(\S+)', header)
		if not g: return
		print 'handshake successful'

	def onConnect(self):
		print 'connection made'
		if self.factory.isFull():
			self.sendMessage('server full')
			self.abortConnection()
		else:
			self.factory.clients.append(self)
			self.name = None
			self.gamekey = None
			self.playerdata = None

	def onMessage(self, raw_data):
		print str(self.name) + " - " + raw_data
		data = raw_data.split()
		try:
			if data[0] == 'quit' and len(data) == 1:
				self.closeConn()

			elif data[0] == serverfuncts.CODES['close connection']:
				self.abortConnection()

			elif data[0] == 'login':
				serverfuncts.login(self, data[1], data[2])
				print 'Players: '+str(self.factory.named_clients.keys())

			elif data[0] == 'logout':
				serverfuncts.logout(self)
				print 'Players: '+str(self.factory.named_clients.keys())
				print 'Games: '+str(self.factory.games)

			elif data[0] == 'create' and data[1] == 'game':
				serverfuncts.createGame(self, data[2])
				print 'Games: '+str(self.factory.games)

			elif data[0] == 'join' and data[1] == 'game':
				serverfuncts.joinGame(self, data[2], self.playerdata)
				print 'Games: '+str(self.factory.games)

			elif data[0] == 'levelup':
				serverfuncts.levelup(self, data[1])

			elif data[0] == 'quit' and data[1] == 'game':
				serverfuncts.quitGame(self)
				print 'Games: '+str(self.factory.games)

			elif data[0] == 'attack':
				gamefuncts.attack(self, data[1])

			elif data[0] == 'defend':
				gamefuncts.defend(self, data[1])

			elif raw_data.strip() == 'get player data': # for debugging
				msg = self.factory.json_encoder.encode(self.playerdata)
				self.sendMessage(msg)

			elif raw_data.strip() == 'get games data': # for debugging
				msg = self.factory.json_encoder.encode(self.factory.games)
				self.sendMessage(msg)

			else:
				self.sendMessage(serverfuncts.CODES['failed'])

		except IndexError as e:
			print e
			self.sendMessage(serverfuncts.CODES['failed'])

		except KeyError as e:
			print e
			self.sendMessage(serverfuncts.CODES['failed'])

	def closeConn(self):
		print 'client closing'
		serverfuncts.onCloseConn(self)

class FEWGServerFactory(ServerFactory):
	def __init__(self, proto, client_limit, game_limit, props):
		self.protocol = proto
		self.client_limit = client_limit
		self.game_limit = game_limit
		self.properties = props

		self.clients = []
		self.named_clients = {}
		self.games = {}

		#self.redis_conn = StrictRedis(host=self.properties['redis_address'], port=self.properties['redis_port'])
		#self.redis_lock = Redlock([{'host': self.properties['redis_address'],'port': self.properties['redis_port']}])

		self.json_decoder = JSONDecoder()
		self.json_encoder = JSONEncoder()

	def isFull(self):
		return len(self.clients) >= self.client_limit

	def sendToAll(self, msg):
		for c in self.clients:
			c.sendMessage(msg)

	def sendToClients(self, clientnames, msg):
		for name in clientnames:
			self.named_clients[name].sendMessage(msg)

from twisted.internet import reactor

class FEWGServer(object):
	def __init__(self, prop_path='server.properties', client_limit=10, game_limit=5):
		self.prop_path = prop_path
		self.properties = storage.readProperties(self.prop_path)
		reactor.addSystemEventTrigger('before', 'shutdown', self.onStop)
		reactor.listenTCP(int(self.properties['server_port']), FEWGServerFactory(FEWGProtocol, client_limit, game_limit, self.properties))

	def start(self):
		reactor.run()

	def onStop(self):
		storage.writeProperties(self.prop_path, self.properties)
