defaultProps = {'server_address':'localhost', 'server_port':'1234', 'redis_port':'6379'}

def writeProperties(filepath, data):
	filestr = ''
	for k in data.keys():
		filestr += k + '=' + data[k] + '\n'

	with f as open(filepath, 'w'):
		f.write(filestr)

def readProperties(filepath):
	data = {}
	for line in open(filepath, 'r'):
		key, val = data.split('=')
		data[key] = val

	for key in defaultProps.keys():
		if key not in data.keys() or data[key].strip() == '':
			data[key] = defaultProps[key]

	if 'redis_address' not in data.keys() or data['redis_address'].strip() == '':
		data['redis_address'] = data['server_address']

	return data
