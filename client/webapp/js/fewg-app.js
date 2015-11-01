(function(){
	var app = angular.module('FEWGApp', 
		['LogModule', 
		'ConnectModule', 
		'LoginModule', 
		'LobbyModule',
		'GameModule',
		'CommandModule']);

	app.controller('ClientCtrl', ['$rootScope', function($rootScope){
		var ctrl = this;

		ctrl.root = $rootScope;

		$rootScope.data = {};
		ctrl.status = 'Connecting';
		ctrl.connected = false;

		ctrl.setData = function(msg){
			$rootScope.$apply(function(){
				$rootScope.data = msg;
			});
		};
		ctrl.setStatus = function(msg){
			if(ctrl.status != msg){
				$rootScope.$apply(function(){
					ctrl.status = msg;
				});
				if(msg == 'In lobby' || msg == 'In game')
					document.getElementById('cmdInput').focus();
				if(msg == 'Logging in')
					document.getElementById('usernameInput').focus();
			}
		};
		ctrl.setConnected = function(is_connected){
			$rootScope.$apply(function(){
				ctrl.connected = is_connected;
			});
		};

		ctrl.updateStatus = function(){
			// Change status based on data
			if($rootScope.data.status == 'logged_out'){
				// Move to logging_in state
				ctrl.setStatus('Logging in');
			}
			else if($rootScope.data.games != undefined){
				// Move to lobby state
				ctrl.setStatus('In lobby');
			}
			else if($rootScope.data.gamedata != undefined){
				// Move to game state
				ctrl.setStatus('In game');
			}
		};

		ctrl.openConn = function(addr, port){
			// Init websocket
			ctrl.ws = new WebSocket('ws://'+addr+':'+port);
			ctrl.ws.onopen = function(){
				// Update status
				ctrl.setStatus('Logging in');
				ctrl.setConnected(true);
				$rootScope.addToLog('log','Connected to server');
			};
			ctrl.ws.onmessage = function(evt){
				// Update data
				ctrl.setData(JSON.parse(evt.data));
				if($rootScope.data.err != undefined) // Log errors
					$rootScope.addToLog('err', $rootScope.data.err);
				if($rootScope.data.message != undefined) // Log server messages
					$rootScope.addToLog('log', $rootScope.data.message);
				if($rootScope.data.chat != undefined) // Log chat messages
					$rootScope.addToLog('chat', $rootScope.data.chat);
				if($rootScope.data.whisper != undefined) // Log whispers
					$rootScope.addToLog('whisper', $rootScope.data.whisper);
				ctrl.updateStatus();
			};
			ctrl.ws.onclose = function(){
				// Update status
				if(ctrl.status == 'Connecting'){
					$rootScope.addToLog('err',
					'Error connecting to game server');
				}
				else{
					ctrl.ws.close();
					ctrl.setStatus('Connecting');
					ctrl.setConnected(false);
					$rootScope.addToLog('log','Disconnected from server');
				}
			};
		};
		$rootScope.connect = function(addr, port){
			// Wrapper for connect module
			ctrl.openConn(addr, port);
		};

		$rootScope.sendMsg = function(msg){
			ctrl.ws.send(msg);
		};

		window.onbeforeunload = function(){
			if(ctrl.connected){
				// Let the server know before leaving
				$rootScope.sendMsg('disconnect');
				ctrl.ws.close();
			}
		};
	}]);
})();