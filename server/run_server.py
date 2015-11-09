import os.path
path = os.path.dirname(__file__)
if path == '': path = '.'

from src import server
server.FEWGServer(path).start()
