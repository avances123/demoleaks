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

 
demoleaksApp.factory('swapFactory', ['$resource',function($resource) {
    return $resource('/api/swaps/:id', {'id':'@id'}, {
        update: {method:'PUT', params: {id: '@id'}},
    });
}]);

demoleaksApp.factory('itemFactory', ['$resource',function($resource) {
    return $resource('/api/items/:id', {'id':'@id'}, {
        update: {method:'PUT', params: {id: '@id'}},
    });
}]);

demoleaksApp.factory('userFactory', ['$resource',function($resource) {
    return $resource('/api/users/:id', {'id':'@id'}, {
        update: {method:'PUT', params: {id: '@id'}},
    });
}]);

demoleaksApp.factory('actionFactory', ['$resource',function($resource) {
    return $resource('/api/actions/:id', {'id':'@id'}, {
        //save: {method:'PUT', params: {id: '@id'}},
    });
}]);

demoleaksApp.factory('swapGisFactory', ['$resource',function($resource) {
    return $resource('/api/gis-swaps/:id', {'id':'@id'}, {
        //update: {method:'PUT', params: {id: '@id'}},
    });
}]);

//Filtros

demoleaksApp.filter('limpiaInventory',function () {
    return function(inventory,offer) {
        var list = [];
        angular.forEach(inventory, function(item1, index1) {
            var ofertado = false;
            angular.forEach(offer, function(item2, index2) {
                if (item1.id == item2)
                {
                    ofertado = true;
                }
            });
            if (ofertado){return true;}
            list.push(item1);
        });
        return list;
    };
});


demoleaksApp.filter('limpiaOffer',function () {
    return function(inventory,offer) {
        var list = [];
        angular.forEach(offer, function(item1, index1) {
            angular.forEach(inventory, function(item2, index2) {
                if (item1 == item2.id)
                {
                    list.push(item2);
                }
            });
        });
        return list;
    };
});

demoleaksApp.filter('m_km',function () {
    return function(distance) {
        return parseInt(parseFloat(distance) / 1000) + ' km';
    };
});

demoleaksApp.filter('limpia_currentUser',function () {
    return function(userlist) {
         if(typeof currentUser === 'undefined'){
            return userlist;
         };
        var new_userlist = [];
        angular.forEach(userlist, function(user, index) {
            if(user.id != currentUser){
                new_userlist.push(user);
            }
        });
        return new_userlist;
    };
});


//https://raw.github.com/sparkalow/angular-truncate/master/src/truncate.js
demoleaksApp.filter('characters', function () {
    return function (input, chars, breakOnWord) {
        if (isNaN(chars)) return input;
        if (chars <= 0) return '';
        if (input && input.length >= chars) {
            input = input.substring(0, chars);

            if (!breakOnWord) {
                var lastspace = input.lastIndexOf(' ');
                //get last space
                if (lastspace !== -1) {
                    input = input.substr(0, lastspace);
                }
            }else{
                while(input.charAt(input.length-1) == ' '){
                    input = input.substr(0, input.length -1);
                }
            }
            return input + '...';
        }
        return input;
    };
});



//http://jsfiddle.net/xncuF/
//We already have a limitTo filter built-in to angular,
//let's make a startFrom filter
demoleaksApp.filter('startFrom', function() {
    return function(input, start) {
        start = +start; //parse to int
        return input.slice(start);
    }
});



var INTEGER_REGEXP = /^-?\d+$/;
demoleaksApp.directive('integer', function() {
    return {
        require: 'ngModel',
        link: function(scope, elm, attrs, ctrl) {
            ctrl.$parsers.unshift(function(viewValue) {
                if (INTEGER_REGEXP.test(viewValue)) {
                    // it is valid
                    ctrl.$setValidity('integer', true);
                    return viewValue;
                } else {
                    // it is invalid, return undefined (no model update)
                    ctrl.$setValidity('integer', false);
                    return undefined;
                }
            });
        }
    };
});

