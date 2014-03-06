swapApp.controller('NavbarCtrl', function NavbarCtrl($scope,$state,$stateParams,$modal) {
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

});