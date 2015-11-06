(function(){
	var app = angular.module('FEWGApp', 
		['LogModule', 
		'ConnectModule', 
		'LoginModule', 
		'LobbyModule',
		'GameModule',
		'CommandModule']);

	app.controller('ClientCtrl', ['$rootScope','$timeout',
	function($rootScope, $timeout){
		var ctrl = this;
		ctrl.root = $rootScope;

		$rootScope.data = {'status':'Connecting'};
		$rootScope.username = '';
		ctrl.lastStatus = '';
		ctrl.connected = false;
		ctrl.gamerunning = false;

		ctrl.setData = function(msg){
			// Set data
			$rootScope.$apply(function(){
				ctrl.lastStatus = $rootScope.data.status;
				$rootScope.data = msg;
			});
		};
		ctrl.setConnected = function(is_connected){
			// Set connected variable
			$rootScope.$apply(function(){
				ctrl.connected = is_connected;
			});
		};
		ctrl.setGameRunning = function(running){
			// Set connected variable
			$rootScope.$apply(function(){
				ctrl.gamerunning = running;
			});
		};
		ctrl.focusInput = function(){
			// Focus input if status is changed
			if($rootScope.data.status != ctrl.lastStatus){
				if($rootScope.data.status == 'In lobby' 
				|| $rootScope.data.status == 'In game')
					document.getElementById('cmdInput').focus();
				if($rootScope.data.status == 'Logging in')
					document.getElementById('usernameInput').focus();
			}
		};
		ctrl.isStatus = function(status){
			// Check status
			return $rootScope.data.status == status;
		};
		ctrl.setCountdown = function(count){
			$rootScope.$apply(function(){
				$rootScope.data.countdown = count;
			});
			$rootScope.addToLog('log',count);
		};
		ctrl.countdown = function(){
			ctrl.setCountdown('3');
			$timeout(function(){ctrl.setCountdown('2');}, 1000, false);
			$timeout(function(){ctrl.setCountdown('1');}, 2000, false);
			$timeout(function(){ctrl.setCountdown('Go!');}, 3000, false);
			$timeout(function(){
				ctrl.setCountdown(undefined);
				ctrl.focusInput()
			}, 4000, false);
		};

		ctrl.openConn = function(addr, port){
			// Init websocket
			ctrl.ws = new WebSocket('ws://'+addr+':'+port);
			ctrl.ws.onopen = function(){
				// Update status
				ctrl.setConnected(true);
				$rootScope.addToLog('log','Connected to server');
			};
			ctrl.ws.onmessage = function(evt){
				// Update data
				ctrl.setData(JSON.parse(evt.data));
				// Add any messages to log
				if($rootScope.data.err != undefined)
					// Log errors
					$rootScope.addToLog('err', $rootScope.data.err);
				if($rootScope.data.message != undefined)
					// Log server messages
					$rootScope.addToLog('log', $rootScope.data.message);
				if($rootScope.data.chat != undefined)
					// Log chat messages
					$rootScope.addToLog('chat', $rootScope.data.chat);
				if($rootScope.data.whisper != undefined)
					// Log whispers
					$rootScope.addToLog('whisper', $rootScope.data.whisper);
				if($rootScope.data.winner != undefined)
					// Log gameover message
					$rootScope.addToLog('log', 'Game over! '
										+$rootScope.data.winner+' wins!');
				// Check start game
				if(ctrl.isStatus('In game')){
					if(Object.keys($rootScope.data.gamedata.players).length 
					== $rootScope.data.gamedata.playerlimit){
						if(!ctrl.gamerunning){
							ctrl.countdown();
							ctrl.setGameRunning(true);
						}
					}
					else
						ctrl.setGameRunning(false);
				}
				else
					ctrl.setGameRunning(false);
				// Give focus to apropriate input
				ctrl.focusInput();
			};
			ctrl.ws.onclose = function(){
				// Update status
				if(!ctrl.connected){
					$rootScope.addToLog('err',
					'Error connecting to game server');
				}
				else{
					ctrl.ws.close();
					ctrl.setData({'status':'Connecting'});
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
			// Send data through root scope
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