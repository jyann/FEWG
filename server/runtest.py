if __name__ == '__main__':
	from os import system
	from sys import argv
	import unittest.main

	if len(argv) > 1:
		if argv[1] == 'gamelogic':
			system('python gamelogic/tests.py')

