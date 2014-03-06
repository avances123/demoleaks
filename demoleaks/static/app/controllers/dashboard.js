swapApp.controller('DashboardCtrl', function DashboardCtrlCtrl($scope,$state,$timeout, $upload,ngProgressLite,swapGisFactory,actionFactory,leafletData, itemFactory,userFactory) {

    if(typeof currentUser == 'undefined'){
        $state.go('users.list');
    };

    $scope.shared={};
    $scope.markers = {};
    $scope.layers = {
        baselayers: {
            stamen: {
                name: 'stamen',
                type: 'xyz',
                url: 'http://{s}.tile.stamen.com/toner-lite/{z}/{x}/{y}.png',
                layerOptions: {
                    subdomains: ['a', 'b', 'c'],
                    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                    continuousWorld: false
                }
            }
        }
    };

    angular.extend($scope, {
        center: {
            lat: 0,
            lng: 0,
            zoom: 12
        }
    });

    $scope.shared.item_form = false;
    if(typeof currentUser != 'undefined'){
        //$scope.items = itemFactory.query({'owner':currentUser});
        $scope.swaplist = swapGisFactory.query({'user':currentUser});
        $scope.actionlist = actionFactory.query({'actor_object_id':currentUser});
        $scope.user = userFactory.get({'id':currentUser});
        $scope.user.$promise.then(function (user) {
            $scope.items = user.items;
        });
        
    };
	




 
    $scope.save_position = function () {
        console.log($scope.markers[$scope.user.id]);
        marker = $scope.markers[$scope.user.id];
        $scope.user.position = "POINT ( "+ marker.lng + " " + marker.lat + " )";
        userFactory.update($scope.user);
    }

    $scope.setmap = function () {
        var re = /[-+]?[0-9]*\.?[0-9]+/g;
        var coords = [];
        if ($scope.user.position){
            coords = $scope.user.position.match(re);
        }
        else{
            coords = [0,0];
        }
        
        $scope.center = {lat:parseFloat(coords[1]),lng:parseFloat(coords[0]),zoom:3}
        $scope.markers[$scope.user.id]= {
	        lat: $scope.center.lat,
	        lng: $scope.center.lng,
	        message: "Arrastrame donde quieras poner tu hogar",
	        focus: true,
	        draggable: true	    
	    };
        leafletData.getMap().then(function(map) {
            map.invalidateSize(false);
        });
        console.log($scope.markers);
    }
    

	

    $scope.delete_item = function(item){
        console.log("Borrando",item);
        //item.owner = item.owner.id;
        itemFactory.delete(item,function () {            
            //Dame exito
            var index = $scope.items.indexOf(item);
            if (index > -1) {
               $scope.items.splice(index, 1);
           }
       });
    };


    $scope.edit_item = function(item){
        console.log(item);
        $scope.selected_item = item;
        $scope.item_name = item.name;
        $scope.item_desc = item.description;
        
    };


    $scope.submit_item = function  () {
        $scope.start(0); //Solo una imagen
    }




    $scope.fileReaderSupported = window.FileReader != null;
    $scope.uploadRightAway = false;

    $scope.onFileSelect = function($files) {
        $scope.selectedFiles = [];
        $scope.progress = [];
        if ($scope.upload && $scope.upload.length > 0) {
            for (var i = 0; i < $scope.upload.length; i++) {
                if ($scope.upload[i] != null) {
                    $scope.upload[i].abort();
                }
            }
        }
        $scope.upload = [];
        $scope.uploadResult = [];
        $scope.selectedFiles = $files;
        $scope.dataUrls = [];
        for ( var i = 0; i < $files.length; i++) {
            var $file = $files[i];
            if (window.FileReader && $file.type.indexOf('image') > -1) {
                var fileReader = new FileReader();
                fileReader.readAsDataURL($files[i]);
                function setPreview(fileReader, index) {
                    fileReader.onload = function(e) {
                        $timeout(function() {
                            $scope.dataUrls[index] = e.target.result;
                        });
                    }
                }
                setPreview(fileReader, i);
            }
            $scope.progress[i] = -1;
            if ($scope.uploadRightAway) {
                $scope.start(i);
            }
        }
    }

    $scope.start = function(index) {
        //nuevo item POST
        if (!$scope.selected_item){
            if($scope.selectedFiles){
                $scope.progress[index] = 0;
                ngProgressLite.start();
                
                $scope.upload[index] = $upload.upload({
                    url : '/api/items',
                    method: 'POST',
                    data : {
                        name : $scope.item_name,
                        description : $scope.item_desc,
                    },
                    file: $scope.selectedFiles[index],
                    fileFormDataName: 'main_photo'
                }).then(function(response) {
                    $scope.items.unshift(response.data);
                    ngProgressLite.done();
                }, function(error) {
                    //console.log(error);
                    ngProgressLite.done();
                }, function(evt) {
                    $scope.progress[index] = parseInt(100.0 * evt.loaded / evt.total);
                    ngProgressLite.set(evt.loaded / evt.total);
                })
            }
            //no tengo imagen
            else{
                console.log("No tengo imagen");
                console.log($scope.item_name,$scope.item_desc,$scope.selectedFiles);
                ngProgressLite.start();
                itemFactory.save({'name':$scope.item_name,'description':$scope.item_desc},
                    function(successResult) {
                        $scope.items.unshift(successResult);        
                        ngProgressLite.done();
                    }, function(errorResult) {
                        ngProgressLite.done();
                        // do something on error
                        if(errorResult.status === 400) {   
                            console.log(errorResult.data.name[0]);         
                        }
                    }
                );
            }
        }
        // updato un item existente
        else
        {
            if($scope.selectedFiles){
                $scope.progress[index] = 0;
                $scope.upload[index] = $upload.upload({
                    url : '/api/items/' + $scope.selected_item.id,
                    method: 'PUT',
                    data : {
                        name : $scope.item_name,
                        description : $scope.item_desc,
                    },
                    file: $scope.selectedFiles[index],
                    fileFormDataName: 'main_photo'
                }).then(function(response) {
                    angular.forEach($scope.items, function(item,i){
                        if($scope.items[i].id === item.id) {
                            $scope.items.splice(i,1);
                            return false;
                        }
                    });
                    $scope.items.unshift(response.data);
                }, null, function(evt) {
                    $scope.progress[index] = parseInt(100.0 * evt.loaded / evt.total);
                })
            }
            else{
                itemFactory.update({'name':$scope.item_name,'description':$scope.item_desc},
                    function(successResult) {
                        angular.forEach($scope.items, function(item,i){
                            if($scope.items[i].id === item.id) {
                                $scope.items.splice(i,1);
                                return false;
                            }
                        });
                        $scope.items.unshift(successResult);        
                    }, function(errorResult) {
                        // do something on error
                        if(errorResult.status === 400) {   
                            console.log(errorResult.data.name[0]);         
                        }
                    }
                );
            }
        }
        
    }
});