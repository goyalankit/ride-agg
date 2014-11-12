var myApp = angular.module('myApp', [
  'ngRoute',
  'inputController'
]);

myApp.config(['$routeProvider', function($routeProvider) {
  $routeProvider.
  when('/input', {
    templateUrl: '/static/partials/user_input.html',
    controller: 'UserInputController'
  }).
  otherwise({
    redirectTo: '/input'
  });
}]);
