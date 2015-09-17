import storage
import rules

from time import sleep

from twisted.internet import protocol
#from redis import StrictRedis
#from redlock import Redlock
from json import JSONDecoder, JSONEncoder

class FEWGProtocol(protocol.Protocol):
	def connectionMade(self):
		if self.factory.isFull():
			self.transport.write('server full\n')
			self.transport.loseConnection()
		else:
			self.factory.clients.append(self)
			self.name = None
			self.gamekey = None

	def dataReceived(self, raw_data):
		data = raw_data.split()
		try:
			if data[0] == 'quit' and len(data) == 1:
				self.closeConn()

			elif data[0] == 'login':
				self = rules.login(data[1], data[2], self)

			elif data[0] == 'logout':
				self = rules.logout(self)

			elif data[0] == 'create' and data[1] == 'game':
				self = rules.createGame(data[2], self)

			elif data[0] == 'join' and data[1] == 'game':
				self = rules.joinGame(data[2], storage.getPlayer(self.name), self)

			elif data[0] == 'quit' and data[1] == 'game':
				self = rules.quitGame(self)

			else:
				self.transport.write(rules.CODES['failed'])

		except IndexError as e:
			self.transport.write(rules.CODES['failed'])

		except KeyError as e:
			self.transport.write(rules.CODES['failed'])

	def closeConn(self):
		self = rules.onCloseConn(self)
		self.transport.loseConnection()

class FEWGServerFactory(protocol.ServerFactory):
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
			c.transport.write(msg)

	def sendToClients(self, clientnames, msg):
		for name in clientnames:
			self.named_clients[name].transport.write(msg)

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
