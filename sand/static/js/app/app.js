var sand = angular.module('sand', ['ngRoute']);

sand.config(['$routeProvider', function($routeProvider) {
    $routeProvider
        .when('/', {
            templateUrl:'static/templates/main.html',
            controller:'MainController'
        })
        .when('/artwork/:artwork_id', {
            templateUrl:'static/templates/artwork.html',
            controller:'ArtworkDetailController'
        });
}]);

sand.run(['$rootScope', '$http', '$q', function($rootScope, $http, $q) {
    $rootScope.load_artworks = function() {
        return $http.get('/api/artworks')
            .success(function(response) {
                $rootScope.artworks = {};
                response.objects.forEach(function(v) {
                    $rootScope.artworks[v.id] = v;
                });
            })
            .error(function(response) {
                console.log("Failed to get artworks:");
                console.log(response);
            });
    };
    $rootScope.load_artworks_if_not_present = function(success_fn) {
        if ($rootScope.artworks === undefined) {
            if (success_fn !== undefined) {
                return $rootScope.load_artworks().success(success_fn);
            } else {
                return $rootScope.load_artworks();
            }

        } else if (success_fn !== undefined) {
            success_fn();
        }
    };
}]);

sand.controller('MainController', ['$scope', '$rootScope', '$http', function($scope, $rootScope, $http) {
    $rootScope.load_artworks_if_not_present();
}]);

sand.controller('ArtworkDetailController', ['$scope', '$rootScope', '$http', '$routeParams', function($scope, $rootScope, $http, $routeParams) {
    $rootScope.load_artworks_if_not_present(function() {
        $scope.artwork = $rootScope.artworks[$routeParams.artwork_id];
    });
}]);
