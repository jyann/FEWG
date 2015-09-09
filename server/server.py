import storage

from twisted.internet import protocol

class FEWGProtocol(protocol.Protocol):
	def connectionMade(self):
		if self.factory.isFull():
			self.transport.write('server full\n')
			self.transport.loseConnection()
		else:
			self.unnamed_clients.append(self)

	def dataReceived(self, raw_data):
		try:
			if data.split()[0] == 'login':
				if not login(data.split()[1], data.split()[2]):
					self.transport.write('login failed\n')
				else:
					self.transport.write('login successful\n')
			else:
				self.transport.write('unknown command\n')
		except Exception:
			self.transport.write('malformed command\n')

	def login(username, password):
		if username in self.factory.names:
			return False
		else:
			self.factory.names.append(username)
			return True

class FEWGServerFactory(protocol.ServerFactory):
	def __init__(self, client_limit):
		self.client_limit = client_limit
		self.clients = []
		self.names = []

	def isFull(self):
		return len(self.clients) >= client_limit

class FEWGServer(object):
	def __init__(self, prop_path='server.properties', client_limit=10):
		from twisted.internet import reactor

		self.prop_path = prop_path
		self.properties = storage.readProperties(self.prop_path)
		reactor.addSystemEventTrigger('before', 'shutdown', self.onStop)
		reactor.listenTCP(int(self.props['server_port']), FEWGServerFactory(client_limit))

	def start(self):
		reactor.run()

	def onStop(self):
		storage.writeProperties(self.prop_path, self.properties)
