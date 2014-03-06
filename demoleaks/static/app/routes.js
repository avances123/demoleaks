demoleaksApp.config(function($stateProvider, $urlRouterProvider,$locationProvider) {

    //$locationProvider.html5Mode(true);
    $locationProvider.hashPrefix('!')

    $urlRouterProvider.otherwise("/elections");

    $stateProvider
      .state('election_list', {
        url: '/elections',
        views: {
          'principal': {
            templateUrl: '/static/app/templates/election_list.html',
            controller: 'ElectionListCtrl'
          }
        }
      })

      .state('election_detail', {
        url: '/election/:id',
        views: {
          'principal': {
            templateUrl: '/static/app/templates/election_detail.html',
            controller: 'ElectionDetailCtrl'
          }
        }
      })


      
  });