(function(){
	var mod = angular.module('ConnectModule', []);
	mod.directive('connectScreen', function(){
		return {
			restrict: 'E',
			templateUrl: 'templates/connect-screen.html',
			controller: ['$rootScope', function($rootScope){
				var ctrl = this;
				
				ctrl.serverAddr = 'localhost'; // Default address
				ctrl.serverPort = '1234'; // Default port

				ctrl.connect = function(){
					$rootScope.connect(ctrl.serverAddr, ctrl.serverPort);
				};
			}],
			controllerAs: 'connectCtrl'
		};
	});
})();