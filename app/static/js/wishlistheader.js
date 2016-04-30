angular.module('WishList').directive('wishlistheader',function(){
    return{
        restrict: 'E',//restricting only to element calls
        templateUrl: "static/templates/header.html"
    }
});
