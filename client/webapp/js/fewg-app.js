(function(){
	var app = angular.module('FEWGApp', []);

	app.controller('ClientCtrl', ['$rootScope', function($rootScope){
		var ctrl = this;

		this.server_addr = 'localhost'; // Default address
		this.server_port = '1234'; // Default port

		this.data = {"status":"disconnected"};
		this.status = 'connecting';
		this.connected = false;
		this.err_msg = '';

		this.clearInputs = function(){
		// Clear inputs after submitting
			ctrl.username = '';
			ctrl.password = '';
			ctrl.lobby_input = '';
			ctrl.game_input = '';
		};

		this.setStatus = function(msg, foc_id){
			$rootScope.$apply(function(){
				ctrl.status = msg;
			});
			document.getElementById(foc_id).focus();
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
		this.setErrMsg = function(msg){
			$rootScope.$apply(function(){
				ctrl.err_msg = msg;
			});
		};

		this.updateStatus = function(){
		// Change status based on data
			if(ctrl.data.status == 'logged_out'
			|| ctrl.data.status == 'connected'){
				// Move to logging_in state
				ctrl.setStatus('logging_in','username_input');
			}
			else if(ctrl.data.status == 'disconnected'){
				// Move to connecting state
				if(ctrl.status == 'connecting')
					ctrl.setErrMsg('Error connecting to game server');
				else
					ctrl.ws.close();
				ctrl.setStatus('connecting','addr_input');
			}
			else if(ctrl.data.games != undefined){
				// Move to lobby state
				ctrl.setStatus('inlobby','lobby_input');
			}
			else if(ctrl.data.gamedata != undefined){
				// Move to game state
				ctrl.setStatus('ingame','game_input');
			}
		};

		this.sendMsg = function(cmd){
			ctrl.ws.send(cmd);
		};
		this.sendInput = function(){
			if(ctrl.status == 'logging_in')
				ctrl.sendMsg('login '+ctrl.username+' '+ctrl.password);
			else if(ctrl.status == 'inlobby')
				ctrl.sendMsg(ctrl.lobby_input);
			else if(ctrl.status == 'ingame')
				ctrl.sendMsg(ctrl.game_input);
			ctrl.clearInputs();
		};

		this.openConn = function(){
		// Init websocket
			ctrl.ws = new WebSocket('ws://'+this.server_addr+':'+this.server_port);
			ctrl.ws.onopen = function(){
				// Update data
				ctrl.setData({"status":"connected"});
				ctrl.setConnected(true);
				ctrl.setErrMsg('');
				ctrl.updateStatus();
			};
			ctrl.ws.onmessage = function(evt){
				// Update data
				ctrl.setData(JSON.parse(evt.data));
				if(ctrl.data.err != undefined)
					// Check for error
					ctrl.setErrMsg(ctrl.data.err);
				else
					// No error
					ctrl.setErrMsg('');
				ctrl.updateStatus();
			};
			ctrl.ws.onclose = function(){
				// Update data
				ctrl.setData({"status":"disconnected"});
				ctrl.setConnected(false);
				ctrl.setErrMsg('');
				ctrl.updateStatus();
			};
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