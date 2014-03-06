swapApp.controller('UserCtrl', function UserCtrl($scope,$state,$stateParams,$modal,ngProgressLite,userFactory,geolocation,leafletData,leafletBoundsHelpers) {

    if ($state.current.name == 'users'){
        $state.go('users.list')
    }



    //Inicializo variables
    $scope.layers = {
        baselayers: {
            stamen: {
                name: 'stamen',
                type: 'xyz',
                url: 'http://{s}.tile.stamen.com/toner-lite/{z}/{x}/{y}.png',
                layerOptions: {
                    subdomains: ['a', 'b', 'c'],
                    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                    continuousWorld: true
                }
            }
            /*nasa: {
                name: 'nasa',
                type: 'wms',
                url: 'http://maps.opengeo.org/geowebcache/service/wms',
                layerOptions: {
                    layers: 'bluemarble',
                    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                    continuousWorld: false
                }
            }*/
        }
    }
    $scope.userlist = [];
    $scope.markers = {};
    $scope.bounds = {};
    $scope.center = {lat: 0,lng: 0, zoom: 2}
    $scope.visitante = {};
    
        

    // LISTENERS
    $scope.$on("leafletDirectiveMap.moveend", function(ev, feat) {
        ngProgressLite.start();
        leafletData.getMap().then(function(map){
            ne = map.getBounds().getNorthEast()
            sw = map.getBounds().getSouthWest()
            //console.log("ORIG",ne_orig,sw_orig)
            
            $scope.userlist = userFactory.query({xmin:sw.lng,ymin:sw.lat,xmax:ne.lng,ymax:ne.lat})
            $scope.userlist.$promise.then($scope.update_markers)
            //ngProgress.reset();
        }); 
        ngProgressLite.done();

    });

    $scope.$on("leafletDirectiveMarker.click", function(ev, feat) {
        console.log(feat)
        $state.go("users.detail",{userId:feat.markerName})
    });

    // Funcion que pasa de WKT de la api a coordenadas del leaflet
    function wkt2leaflet (wkt) {
        var re = /[-+]?[0-9]*\.?[0-9]+/g;
        var coords = wkt.match(re)
        return {lat:parseFloat(coords[1]),lng:parseFloat(coords[0])}
    }

    $scope.update_center_user = function(user) {
        var center = wkt2leaflet(user.position)
        center.zoom=10
        console.log("Poniendo el centro en el user",user,center)
        $scope.center = center
    };
 

    $scope.update_markers = function(userlist) {
        $scope.markers = {};
        //$scope.markers.visitante = $scope.visitante.marker;
        angular.forEach(userlist, function(user, index) {
            if (!user.position) return true; //el return true es un continue
            var coords = wkt2leaflet(user.position)
            //console.log(coords)
            $scope.markers[user.id] = {
                lat: coords.lat,
                lng: coords.lng,
                focus: false,
                title: user.username,
                icon:{
                    type:'awesomeMarker',
                    icon: 'user ',
                    markerColor: 'blue'
                }
            }
            if(typeof currentUser != 'undefined'){
                if (user.id == currentUser) {
                    $scope.markers[user.id] = {
                        lat: coords.lat,
                        lng: coords.lng,
                        focus: true,
                        title: user.username,
                        icon:{
                            type:'awesomeMarker',
                            icon: 'home ',
                            markerColor: 'red'
                        }
                    }
                }
            };
        });
        
    };

    $scope.register = function(){
        $scope.modalInstance = $modal.open({
            templateUrl: '/app/modal_register/',
            controller: 'RegisterCtrl'
        });

        $scope.modalInstance.result.then(function () {
            console.log("Aceptado modal");
        }, function () {
            console.log("Cancelado modal");
        });
    };

    $scope.must_be_registered = function(state,params){
        console.log(state,params);
        if(typeof currentUser != 'undefined'){
            $state.go(state,params);
        } 
        else {
            $scope.register();
        }
    };

});




swapApp.controller('UserListCtrl', function UserListCtrl($scope,$state,$stateParams,userFactory) {
    $scope.center.autoDiscover = true;
    $scope.userlist.$resolved = false;
    $scope.userlist.splice(0, $scope.userlist.length);
});



swapApp.controller('UserDetailCtrl', function UserDetailCtrl($scope,$state,$stateParams,userFactory) {
    $scope.selected_user = {};
    var id = $stateParams['userId']
    $scope.selected_user = userFactory.get({id:id});
    $scope.selected_user.$promise.then(function (user) {
        $scope.update_center_user($scope.selected_user)
    });
});

swapApp.controller('ItemDetailCtrl', function ItemDetailCtrl($scope,$state,$stateParams,itemFactory) {
    $scope.selected_item = {};
    var id = $stateParams['itemId']
    $scope.selected_item = itemFactory.get({id:id});
    $scope.selected_item.$promise.then(function (item) {
        $scope.selected_user = item.owner;
        $scope.update_center_user(item.owner);
    });

});

