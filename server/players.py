perm_stat_defaults = {'health':10,'attack':1,'defense':1,'accuracy':1,'agility':1}
var_stat_defaults = {'health':10,'defense':0,'accuracy':0,'agility':0}

class Player(object):
	def __init__(self):
		self.perm_stats = perm_stat_defaults
		self.var_stats = var_stat_defaults

	def reset_stats(self):
		for vskey in self.var_stats.keys():
			if var_stat_defaults[vskey] == 0:
				self.var_stats[vskey] = 0
			else:
				self.var_stats[vskey] = self.perm_stats[vskey]