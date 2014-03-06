demoleaksApp.controller('ElectionListCtrl', function ElectionListCtrl($scope,$state,$stateParams,electionFactory) {
    console.log("HOLA");
    $scope.electionlist = electionFactory.query({});


});


demoleaksApp.controller('ElectionDetailCtrl', function ElectionDetailCtrl($scope,$state,$stateParams,electionFactory) {

    $scope.election = electionFactory.get({id:$stateParams['id']});


});

