from os import path

defaultProps = {'server_address':'localhost',
				'server_port':'1234',
				'client_limit':'10',
				'game_limit':'5',
				'max_player_limit':'10'}

def writeProperties(filepath, data):
	"""Export server properties (data) to specified file (filepath)."""
	# Form filedata string
	filedata = ''
	for k, v in data.items():
		filedata += k + '=' + v + '\n'
	# Write data to file
	f = open(filepath, 'w')
	f.write(filedata)

def readProperties(filepath):
	"""Read properties from specified file (filepath).
	Any required properties that are not specified are set to default values."""
	# Get data from file
	data = {}
	if path.exists(filepath):
		for line in open(filepath, 'r'):
			if line.strip() != '':
				key, val = line.split('=')
				data[key] = val
	# Set necessary defults
	for key in defaultProps.keys():
		if key not in data.keys() or data[key].strip() == '':
			data[key] = defaultProps[key]

	return data

def getPlayers(filepath, decoder):
	"""Get all players in storage"""
	if path.exists(filepath):
		players = decoder.decode(open(filepath, 'r').read())
	else:
		players = {}
	return players

def getPlayer(filepath, name, decoder):
	"""Get user's player data"""
	players = getPlayers(filepath, decoder)

	if name in players.keys():
		return players[name]
	else:
		return False

def storePlayerData(filepath, name, data, encoder, decoder):
	"""Store user's player data"""
	players = getPlayers(filepath, decoder)
	players[name] = data
	open(filepath, 'w').write(encoder.encode(players))

