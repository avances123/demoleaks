swapApp.config(function($stateProvider, $urlRouterProvider,$locationProvider) {

    //$locationProvider.html5Mode(true);
    $locationProvider.hashPrefix('!')

    $urlRouterProvider.otherwise("/users/list");

    $stateProvider
      .state('xchange', {
        url: '/xchange',
        views: {
          'principal': {
            templateUrl: '/app/xchange/',
            controller: 'XchangeCtrl'
          }
        }
      })

      .state('xchange.new', {
        url: '/with/:withId',
        views: {
          'xchange': {
            templateUrl: '/app/xchange_new/',
            controller: 'NewXchangeCtrl'
          }
        }
      })

      .state('xchange.detail', {
        url: '/:uuid',
        views: {
          'xchange': {
            templateUrl: '/app/xchange_detail/',
            controller: 'DetailXchangeCtrl'
          }
        }
      })

      .state('dashboard', {
        url: '/dashboard',
        views: {
          'principal': {
            templateUrl: '/app/dashboard/',
            controller: 'DashboardCtrl'
          }
        }
      })
      
      
      .state('users', {
        url: '/users',
        views: {
          'principal': {
            templateUrl: '/app/users/',
            controller: 'UserCtrl'
          }
        }
      })
      .state('users.list', {
        url: '/list',
        views: {
          'sidebar': {
            templateUrl: '/app/users_list/',
            controller: 'UserListCtrl'
          }
        }
      })
      .state('users.detail', {
        url: '/:userId',
        views: {
          'sidebar': {
            templateUrl: '/app/users_detail/',
            controller: 'UserDetailCtrl'
          }
        }
      })
      .state('users.itemdetail', {
        url: '/item/:itemId',
        views: {
          'sidebar': {
            templateUrl: '/app/items_detail/',
            controller: 'ItemDetailCtrl'
          }
        }
      })
      .state('swaps', {
        url: '/swaps',
        views: {
          'principal': {
            templateUrl: '/app/swaps/',
            controller: 'SwapCtrl'
          }
        }
      })
      .state('swaps.list', {
        url: '/list',
        views: {
          'sidebar': {
            templateUrl: '/app/swaps_list/',
            controller: 'SwapListCtrl'
          }
        }
      })
      .state('swaps.detail', {
        url: '/:swapId',
        views: {
          'sidebar': {
            templateUrl: '/app/swaps_detail/',
            controller: 'SwapDetailCtrl'
          }
        }
      })


      
  });