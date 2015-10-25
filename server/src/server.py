from serverlogic import storage, serverfuncts, gamefuncts

import re
from TwistedWebsocket.server import Protocol
from twisted.internet.protocol import ServerFactory
from json import JSONDecoder, JSONEncoder

class FEWGProtocol(Protocol):
	"""Websocket protocol for FEWG clients."""
	def onHandshake(self, header):
		"""Overloaded handshake function."""
		g = re.search('Origin\s*:\s*(\S+)', header)
		if not g: return
		print 'handshake successful'

	def onConnect(self):
		"""Overloaded connect function."""
		print 'connection made'
		if self.factory.isFull():
			# Send server full error message
			resp = {}
			resp['err'] = 'The server is full.'
			self.sendMessage(self.factory.json_encoder.encode(resp))
			# Close connection
			self.abortConnection()
		else:
			# Add client to server
			self.factory.clients.append(self)
			# Init client attributes
			self.status = 'logging_in'
			self.name = None
			self.gamekey = None
			self.playerdata = None

	def onMessage(self, raw_data):
		"""Overloaded message function."""
		serverfuncts.logMsg('from: '+str(self.name) + " - " + raw_data)
		# Parse message data
		data = raw_data.split()
		try:
			if data[0] == 'disconnect':
				serverfuncts.closeConn(self)
			elif data[0] == 'login':
				serverfuncts.login(self, data[1], data[2])
			elif data[0] == 'logout':
				serverfuncts.logout(self)
			elif data[0] == 'create' and data[1] == 'game':
				serverfuncts.createGame(self, data[2])
			elif data[0] == 'join' and data[1] == 'game':
				serverfuncts.joinGame(self, data[2])
			elif data[0] == 'levelup':
				serverfuncts.levelup(self, data[1])
			elif data[0] == 'quit' and data[1] == 'game':
				serverfuncts.quitGame(self)
			elif data[0] == 'attack':
				gamefuncts.attack(self, data[1])
			elif data[0] == 'defend':
				gamefuncts.defend(self, data[1])
			else:
				pass

		except IndexError as e:
			# Send error message with status-specific data
			resp = {}
			resp['err'] = 'malformed command'
			serverfuncts.addStatusInfo(self, resp)
			self.sendMessage(self.factory.json_encoder.encode(resp))
			# Log
			serverfuncts.logMsg('to: '+str(self.name)+" - "+str(resp))
			print e

		except KeyError as e:
			# Send error message with status-specific data
			resp = {}
			resp['err'] = 'malformed command'
			serverfuncts.addStatusInfo(self, resp)
			self.sendMessage(self.factory.json_encoder.encode(resp))
			# Log
			serverfuncts.logMsg('to: '+str(self.name)+" - "+str(resp))
			print e

class FEWGServerFactory(ServerFactory):
	"""Websocket factory for FEWG server."""
	def __init__(self, proto, props):
		"""Overloaded constructor."""
		# Link protocol
		self.protocol = proto
		# Set properties
		self.properties = props
		# Init server data
		self.clients = []
		self.named_clients = {}
		self.games = {}
		# Init decoders
		self.json_decoder = JSONDecoder()
		self.json_encoder = JSONEncoder()

	def isFull(self):
		"""Determines if the number of clients has reached its limit.
		Client limit is a server property."""
		return len(self.clients) >= int(self.properties['client_limit'])

	def sendToAll(self, msg):
		"""Send to all connected clients."""
		for c in self.clients:
			c.sendMessage(msg)

	def sendToClients(self, clientnames, msg):
		"""Send to all specified logged in clients."""
		for name in clientnames:
			self.named_clients[name].sendMessage(msg)

from twisted.internet import reactor

class FEWGServer(object):
	"""Server class"""
	def __init__(self, prop_path='server.properties'):
		"""Constructor"""
		# Save properties to pass to factory and to write on shutdown
		self.prop_path = prop_path
		self.properties = storage.readProperties(self.prop_path)
		# Set onstop trigger
		reactor.addSystemEventTrigger('before', 'shutdown', self.onStop)
		# Set up server
		svrfactory = FEWGServerFactory(FEWGProtocol, self.properties)
		reactor.listenTCP(int(self.properties['server_port']), svrfactory)

	def start(self):
		"""Start the server."""
		reactor.run()

	def onStop(self):
		"""Clean up before the server stops."""
		# Store current properties
		storage.writeProperties(self.prop_path, self.properties)
