(function(){
	var app = angular.module('FEWGApp', []);

	app.controller('ClientCtrl', ['$rootScope', function($rootScope){
		var ctrl = this;

		this.server_addr = 'localhost'; // Default address
		this.server_port = '1234'; // Default port

		this.data = {};
		this.status = 'connecting';
		this.connected = false;
		this.err_msg = '';

		this.updateStatus = function(){
			if(ctrl.data.status == 'logged_out'){
				ctrl.setStatus('logging_in');
				document.getElementById('username_input').focus();
			}
			else if(ctrl.data.status == 'disconnected'){
				if(ctrl.status == 'connecting'){
					ctrl.setErrMsg('Error connecting to game server');
				}
				else{
					ctrl.setStatus('connecting');
					ctrl.ws.close();
				}
				document.getElementById('addr_input').focus();
			}
			else if(ctrl.data.games != undefined){
				ctrl.setStatus('inlobby');
				document.getElementById('lobby_input').focus();
			}
			else if(ctrl.data.gamedata != undefined){
				ctrl.setStatus('ingame');
				document.getElementById('game_input').focus();
			}
		};

		this.clearInputs = function(){
			ctrl.username = '';
			ctrl.password = '';
			ctrl.lobby_input = '';
			ctrl.game_input = '';
		};
		this.setStatus = function(msg){
			$rootScope.$apply(function(){
				ctrl.status = msg;
			});
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

		this.openConn = function(){
			ctrl.ws = new WebSocket('ws://'+this.server_addr+':'+this.server_port);
			ctrl.ws.onopen = function(){
				ctrl.setStatus('logging_in');
				ctrl.setData({"status":"connected"});
				ctrl.setConnected(true);
				ctrl.setErrMsg('');
				document.getElementById('username_input').focus();
			};
			ctrl.ws.onmessage = function(evt){
				ctrl.setData(JSON.parse(evt.data));

				if(ctrl.data.err != undefined)
					ctrl.setErrMsg(ctrl.data.err);
				else
					ctrl.setErrMsg('');

				ctrl.updateStatus();
			};
			ctrl.ws.onclose = function(){
				ctrl.setData({"status":"disconnected"});
				ctrl.setConnected(false);
				ctrl.setErrMsg('');
				ctrl.updateStatus();
			};
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

		window.onbeforeunload = function(){
			if(ctrl.connected){
				ctrl.sendMsg('quit');
				ctrl.ws.close();
			}
		};
	}]);
})();