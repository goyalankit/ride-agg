
function autocomplete() {
  var defaultBounds = new google.maps.LatLngBounds(
    new google.maps.LatLng(-33.8902, 151.1759),
    new google.maps.LatLng(-33.8474, 151.2631));
    var src_input = document.getElementById('sourceTextField');
    var dst_input = document.getElementById('destinationTextField');
    var options = {
      country: "India"
    };

    autocomplete1 = new google.maps.places.Autocomplete(src_input, options);
    autocomplete2 = new google.maps.places.Autocomplete(dst_input, options);
}

$(document).ready(function() {
var directionsDisplay;
var directionsService = new google.maps.DirectionsService();
var map;

function initialize() {
  directionsDisplay = new google.maps.DirectionsRenderer();
  var chicago = new google.maps.LatLng(41.850033, -87.6500523);
  var mapOptions = {
    zoom:7,
    center: chicago
  };
  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
  directionsDisplay.setMap(map);
}

function calcRoute() {
  var start = document.getElementById('sourceTextField').value;
  var end = document.getElementById('destinationTextField').value;
  var request = {
      origin:start,
      destination:end,
      travelMode: google.maps.TravelMode.DRIVING,
      unitSystem: google.maps.UnitSystem.METRIC
  };
  directionsService.route(request, function(response, status) {
    if (status == google.maps.DirectionsStatus.OK) {
response.routes[0].legs[0].distance
      directionsDisplay.setDirections(response);
      $r_response = response;
    }
  });

  makeRequestForFares($r_response);
}

function makeRequestForFares(gmap_response) {
    params = []
    for (var i = 0; i < gmap_response.routes.length; i++) {
      for (var j = 0; j < gmap_response.routes[i].legs.length; j++) {
        // remove steps. They are too much data and we don't need it.
        delete gmap_response.routes[i].legs[j].steps
        params.push(gmap_response.routes[i].legs[j]);
      }
    }
    $.post('/', {data: JSON.stringify(params)}, function(result) {
     // ... Process the result ...
    }, 'json');
}

google.maps.event.addDomListener(window, 'load', initialize);

$("#submitbtn")
  .on('click', function(e) {
    // Prevent form submission
    e.preventDefault();

    // Get the form instance
    var $form = $(e.target);
    calcRoute();

    $(".wide").animate({
        height: '50px'
    }, 1000);

//  $( ".inputGroupContainer" ).removeClass("col-md-offset-4", 1000)

    // Use Ajax to submit form data

/*
    $.post($form.attr('action'), $form.serialize(), function(result) {
     // ... Process the result ...
    }, 'json');
*/

  });
});
