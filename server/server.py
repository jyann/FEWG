import storage
import rules

from twisted.internet import protocol
from redis import StrictRedis

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
			if data[0] == 'login':
				self, msg = rules.login(data[1], data[2], self)
				self.transport.write(msg)
			elif data[0] == 'create' and data[1] == 'game':
				self, msg = rules.createGame(data[2], self)
				self.transport.write(msg)				
			elif data[0] == 'join' and data[1] == 'game':
				self, msg = rules.joinGame(data[2], storage.getPlayer(self.name), self)
			else:
				self.transport.write('unknown command\n')
		except Exception as e:
			print e
			self.transport.write('malformed command\n')

class FEWGServerFactory(protocol.ServerFactory):
	def __init__(self, proto, client_limit, game_limit):
		self.protocol = proto
		self.client_limit = client_limit
		self.game_limit = game_limit
		self.clients = []
		self.names = []
		self.games = {}

	def isFull(self):
		return len(self.clients) >= self.client_limit

from twisted.internet import reactor

class FEWGServer(object):
	def __init__(self, prop_path='server.properties', client_limit=10, game_limit=5):
		self.prop_path = prop_path
		self.properties = storage.readProperties(self.prop_path)
		reactor.addSystemEventTrigger('before', 'shutdown', self.onStop)
		reactor.listenTCP(int(self.properties['server_port']), FEWGServerFactory(FEWGProtocol, client_limit, game_limit))
		#redis_conn = StrictRedis(host=self.properties['redis_address'], port=self.properties['redis_port'])

	def start(self):
		reactor.run()

	def onStop(self):
		storage.writeProperties(self.prop_path, self.properties)

if __name__ == '__main__':
	FEWGServer().start()
