
angular.module('WishList').controller('LandingPageController',['$scope','$location','$cookies','$uibModal','APIService',function($scope,$location,$cookies,$uibModal,APIService){
if($cookies.get('loggedIn')=='true'){
    $location.path('/home');
}
}]);
