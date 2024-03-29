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

$vehicle_types = {
  'Olacabs' : {
    'Sedan' : 'Indigo, Dzire, Swift',
    'Mini' : 'Indica',
    'Prime' : 'Ford Icon, Innova, Corolla'
  }

}

var locField;
function getLocation(field) {
    locField = document.getElementById(field);
    console.log("Getting location for the field: " + field);
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
      alert("Failed to get location");
    }
}

function showPosition(position) {
  console.log("Got the location: " + position.coords.latitude + ", " + position.coords.longitude );
  //  var x = document.getElementById(field);
  locField.value = position.coords.latitude + ", " + position.coords.longitude;
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
        $('#main-table-div').show();
        makeRequestForFares(response);
        $("#map-canvas").show();
        google.maps.event.trigger(map, 'resize');
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
        StartLatLng = gmap_response.routes[i].legs[j].start_location
        EndLatLng = gmap_response.routes[i].legs[j].end_location
        gmap_response.routes[i].legs[j].start_location = { k:StartLatLng.lat(), B:StartLatLng.lng() }
        gmap_response.routes[i].legs[j].end_location = { k:EndLatLng.lat(), B:EndLatLng.lng() }
        params.push(gmap_response.routes[i].legs[j]);
      }
    }

        html_string = "<p>Route Distance: <dist>"+ gmap_response.routes[0].legs[0].distance.text +"</p> <p>Estimated Time: "+ gmap_response.routes[0].legs[0].duration.text + "</p>";// ""<p>Route Summary: " + gmap_response.routes[0].summary +"</p>";

        $('#fare-table-div').show();
        $('#dist-data-container').html(html_string);
    // make the post request to server
    $.post('/', {data: JSON.stringify(params)}, function(result) {

        json = result;
        $('#main-table-div').show();
        $('#service-results-table').empty();

        var tr = $("<thead class='service-data-header'> <tr><th>&nbsp;</th> <th>Service</th> <th>Service Type</th> <th>Fare (INR) </th> </tr> </thead>");
        $('#service-results-table').append(tr);
        tr = $('<tr data-toggle="collapse" data-target="#demo0" class="accordion-toggle">');
        tr.append('<td><button class="btn btn-default btn-xs"><span class="glyphicon glyphicon-eye-open"></span></button></td>');
        var count = 0;
        var atLeastOne = false;
        // display results
        for (service in result.fares) {
          if (service == "Olacabs") {
            for (o = 0; o < result.fares[service].length; o++) {
              atLeastOne = true;
              tr.append("<td>" + service + "</td>");
              tr.append("<td>" + result.fares[service][o]["vehicle_type"] + "</td>");
              tr.append("<td>" + Math.round(result.fares[service][o]["fare"]) + " " + "</td>");
              tr.append("</tr>");
              //$('table').append(tr);
              $('#service-results-table').append(tr);

              var created_table = false
              if (typeof result.fares[service][o]["info"] !== "undefined") {
                created_table = true
                tr = $('<tr><td colspan="12" class="hiddenRow"><div class="accordian-body collapse" id="demo'+count+'"> \
                     <table class="table table-striped"><tr><td  class="col-md-3"> <i class="fa fa-clock-o"></i>  <b>Waiting:</b> \
                     ' + result.fares[service][o]["info"] + '"</td><td><i class="glyphicon glyphicon-cog">Night Charges Used</i></td><td class="col-md-3 olabook"><a href="http://www.olacabs.com/">Book the cab</a></td></tr></table></div></td></tr>');
              } else if (typeof result.fares[service][o]["wait_charge_per_min"] !== "undefined"){
                created_table = true
                tr = $('<tr><td colspan="12" class="hiddenRow"><div class="accordian-body collapse" id="demo'+count+'"> \
                     <table class="table table-striped"><tr><td  class="col-md-3"> \
                     ' + " <i class='fa fa-clock-o'></i> <b>Waiting: </b>" + result.fares[service][o]["wait_charge_per_min"] + ' INR per minute</td><td class="col-md-3"><i > <i class="fa fa-car"></i> Vehicle: </i>'+ $vehicle_types[service][result.fares[service][o]["vehicle_type"]] +'</td><td class="col-md-3 olabook"><a href="http://www.olacabs.com/">Book the cab</a></td></tr></table></div></td></tr>');
              } else {
                tr = $('<tr><td colspan="12" class="hiddenRow"><div class="accordian-body collapse" id="demo'+count+'"> \
                     <table class="table table-striped"><tr><td  class="col-md-3"> \
                     ' + " <i class='fa fa-clock-o'></i> <b>Waiting: </b>" + 'No waiting allowed' + '</td><td class="col-md-3"><i > <i class="fa fa-car"></i> Vehicle: </i>'+ $vehicle_types[service][result.fares[service][o]["vehicle_type"]] +'</td><td class="col-md-3 olabook"><a href="http://www.olacabs.com/">Book the cab</a></td></tr></table></div></td></tr>');
              }
              $('#service-results-table').append(tr);
              //$('table').append(tr);
              count = count + 1;
              var str = "<tr data-toggle='collapse' data-target='#demo"+count+"' class='accordion-toggle'>";
              tr = $(str);
              tr.append('<td><button class="btn btn-default btn-xs"><span class="glyphicon glyphicon-eye-open"></span></button></td>');

            }
          }

          if (service == "Uber") {
            for (i = 0; i < result.fares[service].prices.length; i++) {
              atLeastOne = true;
              tr.append("<td>" + service + "</td>");
              tr.append("<td>" + result.fares[service].prices[i].display_name + "</td>");
              tr.append("<td>" + Math.round((parseFloat(result.fares[service].prices[i].high_estimate) + parseFloat(result.fares[service].prices[i].low_estimate)) / 2) + " " + "</td>");
              tr.append("</tr>");
              //$('table').append(tr);
              $('#service-results-table').append(tr);
              tr = $('<tr><td colspan="12" class="hiddenRow"><div class="accordian-body collapse" id="demo'+count+'"> \
                     <table class="table table-striped"><tr><td class="col-md-3"> \
                     <img src="' + result.fares[service].prices[i].image + '" alt="'+ result.fares[service].prices[i].display_name +'"/></td><td class="col-md-3 capacityNumber"> <b>Capacity:</b> '+result.fares[service].prices[i].capacity+'</td> \
                     <td class="col-md-3 capacityNumber"><a href="https://www.uber.com/">Book the cab</a></td></tr></table></div></td></tr>');


              $('#service-results-table').append(tr);
              //$('table').append(tr);
              count = count + 1;
              var str = "<tr data-toggle='collapse' data-target='#demo"+count+"' class='accordion-toggle'>";
              tr = $(str);
              tr.append('<td><button class="btn btn-default btn-xs"><span class="glyphicon glyphicon-eye-open"></span></button></td>');
            }
          }

          if (service == "Meru") {
            for (rec in result.fares[service]) {
              atLeastOne = true;
              tr.append("<td>" + service + "</td>");
              tr.append("<td>" + rec + "</td>");
              tr.append("<td>" + Math.round(result.fares[service][rec]["fare"]) + " " +"</td>");
              tr.append("</tr>");
              $('#service-results-table').append(tr);
              //tr = $('<tr><td colspan="12" class="hiddenRow"><div class="accordian-body collapse" id="demo'+count+'">' + result.fares[service][rec]["rule"]["info"] + "</div></td></tr>");


              // waiting info
              if (typeof result.fares[service][rec]["rule"]["info"] !== "undefined") {
                tr = $('<tr><td colspan="12" class="hiddenRow"><div class="accordian-body collapse" id="demo'+count+'"> \
                     <table class="table table-striped"><tr><td  class="col-md-3"> <i class="fa fa-clock-o"></i>  <b>Waiting:</b> \
                     ' + result.fares[service][rec]["rule"]["info"] + '</td><td class="col-md-3"><i class="fa fa-moon-o">'+ (result.fares[service][rec]["rule"]["night"] == true ? ' Night Charges' : ' Day Charges') +'</i></td><td class="col-md-3 olabook"><a href="http://www.olacabs.com/">Book the cab</a></td></tr></table></div></td></tr>');
              } else if (typeof result.fares[service][rec].rule.wait_charge_per_min !== "undefined"){
                tr = $('<tr><td colspan="12" class="hiddenRow"><div class="accordian-body collapse" id="demo'+count+'"> \
                     <table class="table table-striped"><tr><td  class="col-md-3"> \
                     ' + " <i class='fa fa-clock-o'></i> <b>Waiting: </b>" + result.fares[service][rec].rule.wait_charge_per_min + ' INR per minute</td><td class="col-md-3"><i class="fa fa-moon-o">'+ (result.fares[service][rec]["rule"]["night"] == true ? ' Night Charges' : ' Day Charges') +'</i></td><td class="col-md-3 olabook"><a href="http://www.olacabs.com/">Book the cab</a></td></tr></table></div></td></tr>');
              }

              //$('table').append(tr);
              $('#service-results-table').append(tr);
              count = count + 1;
              var str = "<tr data-toggle='collapse' data-target='#demo"+count+"' class='accordion-toggle'>";
              tr = $(str);
              tr.append('<td><button class="btn btn-default btn-xs"><span class="glyphicon glyphicon-eye-open"></span></button></td>');
            }
          }
        }

        if(!atLeastOne) {
          var dx = document.getElementById("main-table-div");
          dx.innerHTML = "No Results";
        }

    }, 'json');

    //$("service-results-table").tablesorter();
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
