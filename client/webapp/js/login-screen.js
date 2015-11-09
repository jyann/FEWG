(function(){
	var mod = angular.module('LoginModule', []);
	mod.directive('loginScreen', function(){
		return {
			restrict: 'E',
			templateUrl: 'templates/login-screen.html',
			controller: ['$rootScope', function($rootScope){
				var ctrl = this;

				ctrl.username = '';
				ctrl.password = '';

				ctrl.login = function(){
					$rootScope.sendMsg('login '+ctrl.username
						+' '+ctrl.password);
					// Set username
					$rootScope.username = ctrl.username;
					// Reset inputs
					ctrl.username = '';
					ctrl.password = '';
				};
				ctrl.disconnect = function(){
					$rootScope.sendMsg('disconnect');
				};
				ctrl.createUser = function(){
					$rootScope.sendMsg('create user '+ctrl.username
						+' '+ctrl.password);
				};
			}],
			controllerAs: 'loginCtrl'
		};
	});
})();