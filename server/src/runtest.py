import unittest

import gamelogic.tests

def addTestsToSuite(suite, testcase):
	for testname in testcase.testnames:
		suite.addTest(testcase(testname))

	return suite

if __name__ == '__main__':

	from sys import argv

	suite = unittest.TestSuite()

	if len(argv) == 1 or 'all' in argv:
		suite = addTestsToSuite(suite, gamelogic.tests.WaitingRules)
	else:
		if 'game' in argv:
			suite = addTestsToSuite(suite, gamelogic.tests.WaitingRules)

	unittest.TextTestRunner().run(suite)
