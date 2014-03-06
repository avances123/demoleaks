swapApp.controller('RegisterCtrl', function RegisterCtrl($scope,$state,$modalInstance)  {

  $scope.ok = function () {
    $modalInstance.close();
  };

  $scope.cancel = function () {
    $modalInstance.dismiss();
  };
  
});