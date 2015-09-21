# FEWG
##Fight the Enemies, Win the Game!

FEWG is a simple command-based multi-player game.

The server is written in Python and requires Twisted to run.

The client is written in Java.

##1. Client

The client is not yet functional. Check back later!

##2. Server

###1. Setup

1. [Install Python 2.7.10](https://www.python.org/downloads/) if it is not already installed on your system.

2. Make sure that pip is installed. If it is not, [install it.](https://pip.pypa.io/en/stable/installing/)

3. Navigate to the server directory in the project root. If you'd like to use the included virtual environment, run:

`source venv/bin/activate`

Otherwise install the required modules by running:

`pip install twisted`

###2. Running the Server

1. Navigate to the project's root directory and run:

`python run_server.py`
