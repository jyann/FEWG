# FEWG
##Fight the Enemies, Win the Game!

FEWG is a simple command-based multi-player game.

The server is written in Python and requires Twisted and TwistedWebsocket to run.

The client is written in Javascript using WebSockets (requires HTML5). 

##1. Client

In order to use the client, you must know the address 
and port (default is 1234) of the server you plan to connect to.

###1. The web app

Simply open the client webapp in your web browser of choice.
Note that your browser must support HTML5 websockets.

##2. Server

###1. Setup

1. [Install Python 2.7.10](https://www.python.org/downloads/) if it is not already installed on your system.

2. Make sure that pip is installed. If it is not, [install it.](https://pip.pypa.io/en/stable/installing/)

3. To install the required modules, navigate to the server directory in the project root and run:

`pip install twisted`
`pip install -r requirements.txt`

Note that installing from requirements.txt may fail if twisted is not already installed.

###2. Running the Server

1. Navigate to the project's root directory and run:

`python run_server.py`
