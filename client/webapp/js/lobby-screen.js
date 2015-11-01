(function(){
	var mod = angular.module('LobbyModule', []);
	mod.directive('lobbyScreen', function(){
		return {
			restrict: 'E',
			templateUrl: 'templates/lobby-screen.html',
			controller: ['$rootScope', function($rootScope){
				var ctrl = this;
				ctrl.root = $rootScope;

				ctrl.createGameInput = '';

				ctrl.createGame = function(){
					$rootScope.sendMsg('create game '+ctrl.createGameInput);
					ctrl.createGameInput = '';
				};
				ctrl.joinGame = function(gamename){
					$rootScope.sendMsg('join game '+gamename);
				};
				ctrl.logout = function(){
					$rootScope.sendMsg('logout');
				};
				ctrl.disconnect = function(){
					$rootScope.sendMsg('disconnect');
				};
			}],
			controllerAs: 'lobbyCtrl'
		};
	});
})();