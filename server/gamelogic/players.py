stat_defaults = {'health':10,'attack':1,'defense':1}
var_defaults = {'health':10,'defense':0}

class Player(object):
	def __init__(self):
		self.stats = stat_defaults
		self.vars = var_defaults
		self.status = 'waiting'

	def reset_vars(self, varkeys=None):
		if varkeys == None:
			varkeys = self.vars.keys()

		for varkey in varkeys:
			if var_defaults[varkey] == 0:
				self.vars[varkey] = 0
			else:
				self.vars[varkey] = self.stats[varkey]
