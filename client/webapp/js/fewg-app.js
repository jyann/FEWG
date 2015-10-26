(function(){
	var app = angular.module('FEWGApp', []);

	app.controller('ClientCtrl', ['$rootScope', function($rootScope){
		var ctrl = this;

		this.serverAddr = 'localhost'; // Default address
		this.serverPort = '1234'; // Default port

		this.data = {};
		this.status = 'Connecting';
		this.connected = false;
		this.clientlog = [];

		this.clearInputs = function(){
		// Clear inputs after submitting
			ctrl.username = '';
			ctrl.password = '';
			ctrl.createGameInput = '';
			ctrl.cmdInput = '';
		};

		this.setStatus = function(msg){
			$rootScope.$apply(function(){
				ctrl.status = msg;
			});
			if(msg == 'In lobby')
				document.getElementById('cmdInput').focus();
			if(msg == 'In game')
				document.getElementById('cmdInput').focus();
		};
		this.setConnected = function(is_connected){
			$rootScope.$apply(function(){
				ctrl.connected = is_connected;
			});
		}
		this.setData = function(msg){
			$rootScope.$apply(function(){
				ctrl.data = msg;
			});
		};
		this.addToLog = function(type, msg){
			$rootScope.$apply(function(){
				ctrl.clientlog.push({'type':type,'msg':msg});
			});
		};

		this.updateStatus = function(){
		// Change status based on data
			if(ctrl.data.status == 'logged_out'){
				// Move to logging_in state
				ctrl.setStatus('Logging in');
			}
			else if(ctrl.data.games != undefined){
				// Move to lobby state
				ctrl.setStatus('In lobby');
			}
			else if(ctrl.data.gamedata != undefined){
				// Move to game state
				ctrl.setStatus('In game');
			}
		};

		this.sendMsg = function(cmd){
			ctrl.ws.send(cmd);
			ctrl.clearInputs();
		};

		this.openConn = function(){
		// Init websocket
			ctrl.ws = new WebSocket('ws://'+ctrl.serverAddr+':'+ctrl.serverPort);
			ctrl.ws.onopen = function(){
				// Update status
				ctrl.setStatus('Logging in');
				ctrl.setConnected(true);
			};
			ctrl.ws.onmessage = function(evt){
				// Update data
				ctrl.setData(JSON.parse(evt.data));
				if(ctrl.data.err != undefined) // Log errors
					ctrl.addToLog('err', ctrl.data.err);
				if(ctrl.data.svrmsg != undefined) // Log server messages
					ctrl.addToLog('server-message', ctrl.data.svrmsg);
				if(ctrl.data.chat != undefined) // Log chat messages
					ctrl.addToLog('chat', ctrl.data.chat);
				if(ctrl.data.whisper != undefined) // Log whispers
					ctrl.addToLog('whisper', ctrl.data.whisper);
				ctrl.updateStatus();
			};
			ctrl.ws.onclose = function(){
				// Update status
				if(ctrl.status == 'Connecting')
					ctrl.addToLog('err','Error connecting to game server');
				else
					ctrl.ws.close();
				ctrl.setStatus('Connecting');
				ctrl.setConnected(false);
			};
		};

		this.login = function(){
			ctrl.sendMsg('login '+ctrl.username+' '+ctrl.password);
		};
		this.createGame = function(){
			ctrl.sendMsg('create game '+ctrl.createGameInput);
		};

		window.onbeforeunload = function(){
			if(ctrl.connected){
				// Let the server know before leaving
				ctrl.sendMsg('disconnect');
				ctrl.ws.close();
			}
		};
	}]);
})();