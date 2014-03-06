var demoleaksApp = angular.module('demoleaksApp', 
    [
        'ui.router',
        'ngCookies',
        'ngResource',
        'geolocation',
        'leaflet-directive',
        'ui.bootstrap',
        'ngAnimate',
        'ngDisqus',
        'ngProgressLite'
    ]
);


demoleaksApp.run(function ($http, $cookies) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
});

 
demoleaksApp.factory('electionFactory', ['$resource',function($resource) {
    return $resource('/api/elections/:id', {'id':'@id'}, {
        
    });
}]);


