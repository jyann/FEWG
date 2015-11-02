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

		$rootScope.data = {'status':'Connecting'};
		ctrl.lastStatus = '';
		ctrl.connected = false;

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
				if($rootScope.data.err != undefined) // Log errors
					$rootScope.addToLog('err', $rootScope.data.err);
				if($rootScope.data.message != undefined) // Log server messages
					$rootScope.addToLog('log', $rootScope.data.message);
				if($rootScope.data.chat != undefined) // Log chat messages
					$rootScope.addToLog('chat', $rootScope.data.chat);
				if($rootScope.data.whisper != undefined) // Log whispers
					$rootScope.addToLog('whisper', $rootScope.data.whisper);
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