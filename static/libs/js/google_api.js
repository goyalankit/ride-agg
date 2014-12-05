
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
    $("#map-canvas").hide();
    directionsDisplay = new google.maps.DirectionsRenderer();
    var delhi = new google.maps.LatLng(28.6469655,77.0932634);
    var mapOptions = {
      zoom:10,
      center: delhi
    };
    map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
    directionsDisplay.setMap(map);
  }

  function calcRoute() {
    var start = document.getElementById('sourceTextField').value;
    var end   = document.getElementById('destinationTextField').value;
    var request = {
      origin:start,
      destination:end,
      travelMode: google.maps.TravelMode.DRIVING,
      unitSystem: google.maps.UnitSystem.METRIC
    };
    directionsService.route(request, function(response, status) {
      if (status == google.maps.DirectionsStatus.OK) {
        directionsDisplay.setDirections(response);
        $("#map-canvas").show();
        google.maps.event.trigger(map, 'resize');
        setTimeout( makeRequestForFares(response), 0 );
      }
    });
  }


  // TODO(goyalankit) Format the results
  // and check for error conditions
  function makeRequestForFares(_response) {
    var gmap_response = jQuery.extend(true, {}, _response);
    params = []
    for (var i = 0; i < gmap_response.routes.length; i++) {
      for (var j = 0; j < gmap_response.routes[i].legs.length; j++) {
        // remove steps. They are too much data and we don't need it.
        delete gmap_response.routes[i].legs[j].steps
        params.push(gmap_response.routes[i].legs[j]);
      }
    }
    // make the post request to server
    $.post('/', {data: JSON.stringify(params)}, function(result) {
      $('table').empty();
      json = result;
      var tr;
      // display results
      for (service in result.fares) {
        tr = $('<tr/>');
        if (service == "Meru") {
          for (rec in result.fares[service]) {
            tr.append("<td>" + service + "</td>");
            tr.append("<td>" + rec + "</td>");
            tr.append("<td>" + result.fares[service][rec]["fare"] + "</td>");
            $('table').append(tr);
            tr = $('<tr/>');
          }
        }

        if (service == "Uber") {
          for (i = 0; i < result.fares[service].prices.length; i++) {
            tr.append("<td>" + service + "</td>");
            tr.append("<td>" + result.fares[service].prices[i].display_name + "</td>");
            tr.append("<td>" + result.fares[service].prices[i].high_estimate + "</td>");
            $('table').append(tr);
            tr = $('<tr/>');
          }
        }
      }

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

    // send the text field to top
    $(".wide").animate({
      height: '50px'
    }, 1000);
  });
});
