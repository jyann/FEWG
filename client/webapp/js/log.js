(function(){
	var mod = angular.module('LogModule', []);
	mod.directive('log', function(){
		return {
			restrict: 'E',
			templateUrl: 'templates/log.html',
			controller: ['$rootScope', function($rootScope){
				var ctrl = this;
				ctrl.clientlog = [];

				$rootScope.addToLog = function(type, msg){
					$rootScope.$apply(function(){
						ctrl.clientlog.push({'type':type,'msg':msg});
					});
				};
			}],
			controllerAs: 'logCtrl'
		};
	});
})();