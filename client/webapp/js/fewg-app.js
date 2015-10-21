(function(){
	var app = angular.module('FEWGApp', []);

	app.controller('ClientCtrl', ['$rootScope', function($rootScope){
		var ctrl = this;
		
		this.data = {};
		this.status = 'connecting';
		this.err_msg = '';

		this.updateStatus = function(){
			if(ctrl.data.status == 'logged_out')
				ctrl.status = 'logging_in';
			else if(ctrl.data.status == 'disconnected')
				ctrl.status = 'connecting';
			else if(ctrl.data.games != undefined)
				ctrl.status = 'inlobby';
			else if(ctrl.data.gamedata != undefined)
				ctrl.status = 'ingame';
		};
		
		this.setStatus = function(msg){
			$rootScope.$apply(function(){
				ctrl.status = msg
			});
		};
		this.setData = function(msg){
			$rootScope.$apply(function(){
				ctrl.data = msg
			});
		};
		this.setErrMsg = function(msg){
			$rootScope.$apply(function(){
				ctrl.err_msg = msg
			});
		};

		this.openConn = function(){
			this.ws = new WebSocket('ws://'+this.server_addr+':'+this.server_port);
			this.ws.onopen = function(msg){
				ctrl.setStatus('logging_in');
				ctrl.setData();
				ctrl.setErrMsg('');
			};
			this.ws.onmessage = function(msg){
				ctrl.setData(JSON.parse(msg.data));
				
				if(ctrl.data.err != undefined)
					ctrl.setErrMsg(ctrl.data.err);
				else
					ctrl.setErrMsg('');

				ctrl.updateStatus();
			};
			this.ws.onerror = function(msg){
				ctrl.setErrMsg('connection error');
			};
			this.ws.onclose = function(msg){
				ctrl.setStatus('connecting');
			};
		};
		this.sendInput = function(){
			this.ws.send(this.input);
		}
	}]);
})();