(function(){
	var mod = angular.module('CommandModule', []);
	mod.directive('commandForm', function(){
		return {
			restrict: 'E',
			templateUrl: 'templates/command-form.html',
			controller: ['$rootScope', function($rootScope){
				var ctrl = this;
				ctrl.root = $rootScope;

				ctrl.cmdInput = '';

				ctrl.sendCommand = function(){
					$rootScope.sendMsg(ctrl.cmdInput);
					ctrl.cmdInput = '';
				};
			}],
			controllerAs: 'commandCtrl'
		};
	});
})();