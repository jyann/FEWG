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
					ctrl.username = '';
					ctrl.password = '';
				};
				ctrl.disconnect = function(){
					$rootScope.sendMsg('disconnect');
				};
			}],
			controllerAs: 'loginCtrl'
		};
	});
})();