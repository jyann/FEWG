import unittest

import gamelogic.tests

def addTestsToSuite(suite, testcase):
	for testname in testcase.testnames:
		suite.addTest(testcase(testname))

	return suite

if __name__ == '__main__':

	from sys import argv

	suite = unittest.TestSuite()

	if len(argv) > 1:
		if argv[1] == 'gamelogic':
			suite = addTestsToSuite(suite, gamelogic.tests.GameTest)
		else:
			print 'Invalid argument'
	else:
		suite = addTestsToSuite(suite, gamelogic.tests.GameTest)

	unittest.TextTestRunner().run(suite)
