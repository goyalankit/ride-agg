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
    //setUpInitialTable();
}

function create_table_entry() {
  var tr = $('<tr data-toggle="collapse" data-target="#demo1" class="accordion-toggle">');
  tr.append('<td><button class="btn btn-default btn-xs"><span class="glyphicon glyphicon-eye-open"></span></button></td>');
  return tr;
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
      center: delhi,
       styles: [{"featureType":"landscape","stylers":[{"saturation":-100},{"lightness":65},{"visibility":"on"}]},{"featureType":"poi","stylers":[{"saturation":-100},{"lightness":51},{"visibility":"simplified"}]},{"featureType":"road.highway","stylers":[{"saturation":-100},{"visibility":"simplified"}]},{"featureType":"road.arterial","stylers":[{"saturation":-100},{"lightness":30},{"visibility":"on"}]},{"featureType":"road.local","stylers":[{"saturation":-100},{"lightness":40},{"visibility":"on"}]},{"featureType":"transit","stylers":[{"saturation":-100},{"visibility":"simplified"}]},{"featureType":"administrative.province","stylers":[{"visibility":"off"}]},{"featureType":"water","elementType":"labels","stylers":[{"visibility":"on"},{"lightness":-25},{"saturation":-100}]},{"featureType":"water","elementType":"geometry","stylers":[{"hue":"#ffff00"},{"lightness":-25},{"saturation":-97}]}]
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
      json = result;
        $('#main-table-div').show();
        var tr = $("<thead class='service-data-header'> <tr><th>&nbsp;</th> <th>Service</th> <th>Service Type</th> <th>Fare</th> </tr> </thead>");
        $('#service-results-table').append(tr);
        tr = $('<tr data-toggle="collapse" data-target="#demo0" class="accordion-toggle">');
        tr.append('<td><button class="btn btn-default btn-xs"><span class="glyphicon glyphicon-eye-open"></span></button></td>');
        var count = 0;
        // display results
        for (service in result.fares) {
          if (service == "Meru" || service == "Olacabs") {
            for (rec in result.fares[service]) {
              tr.append("<td>" + service + "</td>");
              tr.append("<td>" + rec + "</td>");
              tr.append("<td>" + result.fares[service][rec]["fare"] + "</td>");
              tr.append("</tr>");
              $('#service-results-table').append(tr);
              //tr = $('<tr><td colspan="12" class="hiddenRow"><div class="accordian-body collapse" id="demo'+count+'">' + result.fares[service][rec]["rule"]["info"] + "</div></td></tr>");

              // waiting info
              if (typeof result.fares[service][rec]["rule"]["info"] !== "undefined") {
                tr = $('<tr><td colspan="12" class="hiddenRow"><div class="accordian-body collapse" id="demo'+count+'"> \
                     <table class="table table-striped"><tr><td  class="col-md-4"> <i class="fa fa-clock-o"></i>  <b>Waiting:</b> \
                     ' + result.fares[service][rec]["rule"]["info"] + '"</td><td><i class="glyphicon glyphicon-cog">Night Charges Used</i></td></tr></table></div></td></tr>');
              } else if (typeof result.fares[service][rec].rule.wait_charge_per_min !== "undefined"){
                tr = $('<tr><td colspan="12" class="hiddenRow"><div class="accordian-body collapse" id="demo'+count+'"> \
                     <table class="table table-striped"><tr><td  class="col-md-4"> \
                     ' + " <i class='fa fa-clock-o'></i> <b>Waiting: </b>" + result.fares[service][rec].rule.wait_charge_per_min + ' INR per minute</td><td><i class="glyphicon glyphicon-cog">Night Charges Used</i></td></tr></table></div></td></tr>');
              }

              //$('table').append(tr);
              $('#service-results-table').append(tr);
              count = count + 1;
              var str = "<tr data-toggle='collapse' data-target='#demo"+count+"' class='accordion-toggle'>";
              tr = $(str);
              tr.append('<td><button class="btn btn-default btn-xs"><span class="glyphicon glyphicon-eye-open"></span></button></td>');
            }
          }

          if (service == "Uber") {
            for (i = 0; i < result.fares[service].prices.length; i++) {
              tr.append("<td>" + service + "</td>");
              tr.append("<td>" + result.fares[service].prices[i].display_name + "</td>");
              tr.append("<td>" + result.fares[service].prices[i].high_estimate + " " + result.fares[service].prices[i].currency_code + "</td>");
              tr.append("</tr>");
              //$('table').append(tr);
              $('#service-results-table').append(tr);
              tr = $('<tr><td colspan="12" class="hiddenRow"><div class="accordian-body collapse" id="demo'+count+'"> \
                     <table class="table table-striped"><tr><td class="col-md-3"> \
                     <img src="' + result.fares[service].prices[i].image + '"</td><td class="col-md-3 capacityNumber"> <b>Capacity:</b> '+result.fares[service].prices[i].capacity+'</td> \
                     <td class="col-md-3 capacityNumber"><a href="https://www.uber.com/">Book the cab</a></td></tr></table></div></td></tr>');


              $('#service-results-table').append(tr);
              //$('table').append(tr);
              count = count + 1;
              var str = "<tr data-toggle='collapse' data-target='#demo"+count+"' class='accordion-toggle'>";
              tr = $(str);
              tr.append('<td><button class="btn btn-default btn-xs"><span class="glyphicon glyphicon-eye-open"></span></button></td>');
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
