(function(){
	var mod = angular.module('GameModule', []);
	mod.directive('gameScreen', function(){
		return {
			restrict: 'E',
			templateUrl: 'templates/game-screen.html',
			controller: ['$rootScope', function($rootScope){
				var ctrl = this;
				ctrl.root = $rootScope;

				ctrl.quitGame = function(){
					$rootScope.sendMsg('quit game');
				};
				ctrl.logout = function(){
					$rootScope.sendMsg('logout');
				};
				ctrl.disconnect = function(){
					$rootScope.sendMsg('disconnect');
				};
			}],
			controllerAs: 'gameCtrl'
		};
	});
})();