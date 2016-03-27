var app = angular.module("WishList",['ngRoute','ui.bootstrap']);

app.config(function($routeProvider){
    $routeProvider
    .when('/home',{
        templateUrl: 'static/templates/home.html',
        access: {
            restricted: true
        }
    })
    .when('/login',{
        templateUrl: 'static/templates/login.html',
        controller: 'LoginController',
        access: {
            restricted: false
        }
    })
    .when('/logout',{
        templateUrl: 'static/index.html',
        controller: 'LogoutController',
        access: {
            restricted: true
        }
    })
    .when('/signup',{
        templateUrl: 'static/templates/signup.html',
        controller: 'SignUpController',
        access: {
            restricted: false
        }
    })
    .when('/wish',{
        templateUrl: 'static/templates/newwish.html',
        controller: 'NewWishController',
        access: {
            restricted: true
        }
    })
    
});
