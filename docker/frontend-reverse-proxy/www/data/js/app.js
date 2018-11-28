angular.module('app', ['components'])

  .controller('IndexController', function ($scope, $locale, $http) {

    $scope.prepareIndex = function () {
      $http({
        method: 'GET',
        url: '/training/indexer/reindex'
      }).then(function successCallback(response) {
        console.log(response);
        alert(response.data)
      }, function errorCallback(response) {
        console.log(response);
      });
      alert("Indexing started ... please wait");
    };


  })

  .controller('LabelController', function ($scope, $locale, $http) {

    $scope.label_values = []

    $http({
      method: 'GET',
      url: '/training/labeller/labels'
    }).then(function successCallback(response) {
      console.log(response);
      $scope.labels = response.data
      $scope.label_index = 0
      $scope.q = $scope.labels[$scope.label_index]
      $scope.search()
    }, function errorCallback(response) {
      console.log(response);
    });

    $scope.search = function () {
      $http({
        method: 'GET',
        url: '/training/labeller/search?q=' + $scope.q
      }).then(function successCallback(response) {

        $scope.items = []
        response.data.forEach(element => {
          $scope.items.push({ 'query': $scope.q, 'query_id': $scope.label_index, 'name': element.name, 'id': element.id, 'rating': -1 })
        });

      }, function errorCallback(response) {
        console.log(response);
      });
    };

    $scope.next = function () {
      $scope.label_index++
      $scope.q = $scope.labels[$scope.label_index]
      console.log('len ' + $scope.label_values.length)
      if ($scope.label_index + 1 <= $scope.label_values.length) {
        console.log('index ' + $scope.label_index)
        $scope.items = $scope.label_values[$scope.label_index]
      }
      else {
        if ($scope.label_index > $scope.label_values.length) {
          $scope.label_values.push($scope.items)
        }
        console.log($scope.label_values)
        console.log('index ' + $scope.label_index)
        $scope.search()
      }


      $scope.last = ($scope.label_index === $scope.labels.length - 1)
    };

    $scope.previous = function () {
      if ($scope.label_index === 0) {
        return;
      }

      $scope.label_index--
      console.log('index ' + $scope.label_index)
      $scope.items = $scope.label_values[$scope.label_index]
      $scope.q = $scope.labels[$scope.label_index]
      $scope.last = ($scope.label_index === $scope.labels.length - 1)
    };

    $scope.save = function () {

      var ratings = []
      var queries = []
      var queries_id = []
      $scope.label_values.forEach(element => {
        element.forEach(item => {
          if (item.rating != -1) {
            ratings.push(item)
            if (!queries_id.includes(item.query_id)) {
              queries_id.push(item.query_id)
            }
          }
        })
      });

      $scope.labels.forEach(function (query, i) {
        if (queries_id.includes(i)) {
          queries.push({ 'query': query, 'index': i });
        }
      });

      $http({
        method: 'POST',
        url: '/training/labeller/save',
        heders: { 'Content-Type': 'application/json' },
        data: angular.toJson({ 'queries': queries, 'ratings': ratings })
      }).then(function successCallback(response) {
        console.log(response)
      }, function errorCallback(response) {
        console.log(response);
        alert('ERROR')
      });
    };

  })

  .controller('TrainController', function ($scope, $locale, $http) {

    $scope.train = function () {
      $http({
        method: 'GET',
        url: '/training/trainer/train'
      }).then(function successCallback(response) {
        console.log(response);
        alert(response.data)
      }, function errorCallback(response) {
        console.log(response);
        alert('ERROR')
      });
      alert("Training started ... please wait");
    };


  })

  .controller('TestController', function ($scope, $locale, $http) {

    $scope.test = function () {
      $http({
        method: 'GET',
        url: '/training/tester/test?q=' + $scope.q
      }).then(function successCallback(response) {
        console.log(response);
        $scope.items = response.data
      }, function errorCallback(response) {
        console.log(response);
      });
    };


  });