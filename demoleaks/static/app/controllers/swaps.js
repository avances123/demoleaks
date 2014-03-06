swapApp.controller('SwapCtrl', function SwapCtrl($scope,$state,$stateParams,ngProgressLite,swapGisFactory, swapFactory,geolocation,leafletData,leafletBoundsHelpers) {

    if ($state.current.name == 'swaps'){
        $state.go('swaps.list')
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
    $scope.swaplist = [];
    $scope.bounds = {};
    $scope.paths = {};
    $scope.center = {lat: 0,lng: 0, zoom: 2}
    $scope.visitante = {};
    
        

    // LISTENERS
    $scope.$on("leafletDirectiveMap.moveend", function(ev, feat) {
        leafletData.getMap().then(function(map){
            ne = map.getBounds().getNorthEast()
            sw = map.getBounds().getSouthWest()
            //console.log("ORIG",ne_orig,sw_orig)
            ngProgressLite.start();
            $scope.swaplist = swapGisFactory.query({xmin:sw.lng,ymin:sw.lat,xmax:ne.lng,ymax:ne.lat});
            $scope.swaplist.$promise.then($scope.update_markers);
            ngProgressLite.done();
            
        }); 
        
    });

    $scope.$on("leafletDirectiveMarker.click", function(ev, feat) {
        console.log(feat)
        $state.go("swaps.detail",{swapId:feat.markerName})
    });

    // Funcion que pasa de WKT de la api a coordenadas del leaflet
    function wkt2leaflet (wkt) {
        var re = /[-+]?[0-9]*\.?[0-9]+/g;
        var coords = wkt.match(re)
        return {lat:parseFloat(coords[1]),lng:parseFloat(coords[0])}
    }

    $scope.update_center_swap = function(swap) {
        var coords1 = wkt2leaflet(swap.user1.position)
        var coords2 = wkt2leaflet(swap.user2.position)
        leafletData.getMap().then(function(map) {
            map.fitBounds([ coords1, coords2 ]);
        });
    }
 

    $scope.update_markers = function(swaplist) {

        $scope.paths = {};
        //$scope.markers.visitante = $scope.visitante.marker;
        angular.forEach(swaplist, function(swap, index) {
            if (!swap.user1.position || !swap.user2.position) return true; //el return true es un continue
            var users = [swap.user1,swap.user2];
            var swapcoords=[];
            angular.forEach(users, function(user, index) {
                var coords = wkt2leaflet(user.position)
                swapcoords.push(coords);
                $scope.paths['users_' + user.id] = {
                    color:'#00FFFF',
                    weight: 2,
                    latlngs: coords,
                    type: 'circleMarker',
                    radius: 3
                }
            });
            $scope.paths['swaps_' + swap.id] = {
                color:'#0000FF',
                weight: 2,
                //opacity: 0.5,
                latlngs: swapcoords
            }
        });
    }

});

swapApp.controller('SwapListCtrl', function SwapListCtrl($scope,$state,$stateParams) {
    $scope.center.autoDiscover = true;
    $scope.swaplist.$resolved = false;
    $scope.swaplist.splice(0, $scope.swaplist.length);
});



swapApp.controller('SwapDetailCtrl', function SwapDetailCtrl($scope,$state,$stateParams,swapFactory) {
    $scope.selected_swap = {};
    var id = $stateParams['swapId']
    $scope.selected_swap = swapFactory.get({id:id});
    $scope.selected_swap.$promise.then(function (swap) {
        $scope.update_center_swap($scope.selected_swap)
    });


});
