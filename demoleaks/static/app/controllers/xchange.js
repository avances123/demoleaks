swapApp.controller('XchangeCtrl', function XchangeCtrl($scope,$state,swapFactory, itemFactory,userFactory) {

    $scope.currentPage_inv1 = 1;
    $scope.currentPage_inv2 = 1;
    $scope.pageSize = 12;
    $scope.user1_collapse = true;
    $scope.user2_collapse = true;
    $scope.chat_collapse = true;
    $scope.shared = {};
    $scope.shared.alerts = [];
    $scope.shared.swap_modified = false;
    $scope.swap = {
        ok1:false,
        ok2:false,
        user1:0,
        user2:0,
        items1: [],
        items2: [],
        money1: 0,
        money2: 0
    };


    $scope.do_offer1 = function(item){
        $scope.swap.items1.push(item.id);
        $scope.shared.swap_modified = true;
    };

    $scope.do_offer2 = function(item){
        $scope.swap.items2.push(item.id);
        $scope.shared.swap_modified = true;
    };

    $scope.undo_offer1 = function(index,item){
        $scope.swap.items1.splice(index, 1);
        $scope.shared.swap_modified = true;
    };

    $scope.undo_offer2 = function(index,item){
        $scope.swap.items2.splice(index, 1);
        $scope.shared.swap_modified = true;
    };

    $scope.cancel_swap = function(swap){
        swapFactory.delete(swap);
        $state.go("users.list");
    };

    $scope.preload_tooltip_images = function(user){
        angular.forEach(user.items, function(item, index) {
            //console.log("Metiendo:",item.medium_photo)
            new Image().src = item.medium_photo;
        });
    };

    $scope.closeAlert = function(index) {
        $scope.shared.alerts.splice(index, 1);
    };

});

swapApp.controller('NewXchangeCtrl', function NewXchangeCtrl($scope,$state,$stateParams,swapFactory, itemFactory,userFactory) {
    if(typeof currentUser == 'undefined'){
        $state.go('swaps.list');
    };
    var withId = $stateParams['withId']
    $scope.user1 = userFactory.get({id:currentUser});
    $scope.user2 = userFactory.get({id:withId});
    $scope.user1.$promise.then(function (user) {
        $scope.swap.user1 = $scope.user1.id;
        $scope.preload_tooltip_images(user);
    });
    $scope.user2.$promise.then(function (user) {
        $scope.swap.user2 = $scope.user2.id;
        $scope.preload_tooltip_images(user);
    });

    $scope.submit_swap = function(swap){
        swap.ok1 = true;
        new_swap = swapFactory.save(swap); 
        new_swap.$promise.then(function (swap) {
            $scope.shared.swap_modified = false;
            $state.go("xchange.detail",{ uuid: swap.uuid})
        });
    };
});


swapApp.controller('DetailXchangeCtrl', function DetailXchangeCtrl($scope,$state,$modal,$stateParams,swapFactory, itemFactory,userFactory) {
    if(typeof currentUser == 'undefined'){
        currentUser = 0;
    };
    window.disqus_shortname = 'swapr';
    var uuid = $stateParams['uuid'];
    var promise_swap = swapFactory.query({uuid:uuid})
    $scope.swap_disabled = true;
    promise_swap.$promise.then(function (swap_list) {
        swap = swap_list[0];  //OJO, PARA BUSCAR POR UUID DEVUELVE UNA LISTA
        $scope.swap.id = swap.id;
        $scope.swap.uuid = swap.uuid;
        $scope.swap.ok1 = swap.ok1;
        $scope.swap.ok2 = swap.ok2;
        $scope.swap.items1 = swap.items1;
        $scope.swap.items2 = swap.items2;
        $scope.user1 = userFactory.get({id:swap.user1});
        $scope.user1.$promise.then(function (user) {
            $scope.swap.user1 = $scope.user1.id;
            $scope.preload_tooltip_images(user);
        });
        $scope.user2 = userFactory.get({id:swap.user2});
        $scope.user2.$promise.then(function (user) {
            $scope.swap.user2 = $scope.user2.id;
            $scope.preload_tooltip_images(user);
        });
        console.log($scope.swap)
        // Veo a ver si estoy a la izquierda o a la derecha
        if (currentUser == swap.user1){
            $scope.im_user1 = true;
            $scope.im_user2 = false;
            $scope.swap_disabled = false;
        }
        else if (currentUser == swap.user2){
            $scope.im_user1 = false;
            $scope.im_user2 = true;   
            $scope.swap_disabled = false;
        }
        else {

        }
    });
    
    $scope.submit_swap = function(swap){
        if ($scope.im_user1) {
            $scope.swap.ok1 = true;
            $scope.swap.ok2 = false;
        } else{
            $scope.swap.ok1 = false;
            $scope.swap.ok2 = true;
        };
        swapFactory.update(swap,
            //exito
            function (swap) {
                $scope.swap = swap;
                $scope.shared.swap_modified = false;
                if ($scope.im_user1) {
                    $scope.shared.alerts.push(
                        { 
                            msg: "Esperando a " + $scope.user2.username + ", le hemos enviado un email",
                            type: 'warning',
                        }
                    );
                } else {
                    $scope.shared.alerts.push(
                        { 
                            msg: "Esperando a " + $scope.user1.username + ", le hemos enviado un email",
                            type: 'warning',
                        }
                    );
                }
            },
            //fracaso
            function (errorObj) {
                $scope.swap_modified = true;
                console.log(errorObj);
                $scope.shared.alerts.push(
                    { 
                        msg: errorObj.data,
                        type: 'danger',
                    }
                );
            }
        );
        
    };


    $scope.accept_swap = function(swap){
        $scope.modalInstance = $modal.open({
            templateUrl: 'modal_accept.html',
            controller: ModalInstanceCtrl,
            resolve: {
                swap: function () {
                    return $scope.swap;
                }
            }
        });

        $scope.modalInstance.result.then(function (selectedItem) {
            if ($scope.im_user1) {
                $scope.swap.ok1 = true;
            } else{
                $scope.swap.ok2 = true;
            };
            swapFactory.update(swap);
            $scope.swap_disabled = true;  
        }, function () {
            
        });
    };


    $scope.chat = function(swap){
        $scope.modalInstance = $modal.open({
            templateUrl: 'chat.html',
            controller: ModalInstanceCtrl,
            resolve: {
                swap: function () {
                    return swap;
                }
            }
        });

    };


});


var ModalInstanceCtrl = function ($scope, $modalInstance, swap) {
  $scope.swap = swap;
  console.log($scope.swap.uuid);
  $scope.modal_ok = function () {
    $modalInstance.close();
  };

  $scope.modal_cancel = function () {
    $modalInstance.dismiss();
  };
};

