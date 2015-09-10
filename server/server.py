import storage

from twisted.internet import protocol
from redis import StrictRedis

class FEWGProtocol(protocol.Protocol):
	def connectionMade(self):
		if self.factory.isFull():
			self.transport.write('server full\n')
			self.transport.loseConnection()
		else:
			self.unnamed_clients.append(self)
			self.name = None

	def dataReceived(self, raw_data):
		data = raw_data.split()
		try:
			if data[0] == 'login':
				if not login(data[1], data[2]):
					self.transport.write('login failed\n')
				else:
					self.transport.write('login successful\n')
			elif data[0] == 'create' and data[1] == 'game':
				self.factory.games[data[2]] = {'players':{}}
			elif data[0] == 'join' and data[1] == 'game':
				self.factory.games[data]['players'][self.name] = storage.getPlayer(self.name)
			else:
				self.transport.write('unknown command\n')
		except Exception:
			self.transport.write('malformed command\n')

	def login(username, password):
		if username in self.factory.names:
			return False
		else:
			self.name = username
			self.factory.names.append(username)
			return True

class FEWGServerFactory(protocol.ServerFactory):
	def __init__(self, client_limit, game_limit):
		self.client_limit = client_limit
		self.game_limit = game_limit
		self.clients = []
		self.names = []
		self.games = {}

	def isFull(self):
		return len(self.clients) >= client_limit

class FEWGServer(object):
	def __init__(self, prop_path='server.properties', client_limit=10, game_limit=5):
		from twisted.internet import reactor

		self.prop_path = prop_path
		self.properties = storage.readProperties(self.prop_path)
		reactor.addSystemEventTrigger('before', 'shutdown', self.onStop)
		reactor.listenTCP(int(self.properties['server_port']), FEWGServerFactory(client_limit, game_limit))
		#redis_conn = StrictRedis(host=self.properties['redis_address'], port=self.properties['redis_port'])

	def start(self):
		reactor.run()

	def onStop(self):
		storage.writeProperties(self.prop_path, self.properties)
