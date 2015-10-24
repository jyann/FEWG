from os import path

defaultProps = {'server_address':'localhost','server_port':'1234','client_limit':'10', 'game_limit':'5', 'max_player_limit':'10'}

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

def getPlayer(name):
"""Get user's player data"""
	player = {'name':name,'stats':{},'vars':{},'exp':0}

	player['stats']['health'] = 10
	player['vars']['health'] = 10

	player['stats']['attack'] = 1
	
	player['stats']['defense'] = 1
	player['vars']['defense'] = 0

	return player

def storePlayerData(name, data):
"""Store user's player data"""
	pass
