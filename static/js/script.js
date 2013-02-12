//This is the code to bring the map up and parse in the data from the searchbar taken from the Google Maps V3 API documentation with slight modification
  var geocoder;
  var map;
  var home;
  var events;

function initialize(eventArray) {
  geocoder = new google.maps.Geocoder();
    var myOptions = {
      zoom: 14,
      mapTypeId: google.maps.MapTypeId.SATELLITE
    }
    map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

    events = eventArray;
    for (var i = 0; i < events.length; i++) {
        addMarker(events[i])
    }

}

function addMarker(events){
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(events[3], events[2]),
            map: map,
            title: events[0] + ' @ ' + events[1],
            zIndex: 5
        });
        var infoWindowContent = marker.title + '<br>' + '<center><a href="' + events[4] +'">More info</a></center>';
        $('#events').append('<li>' +  events[0] + ' @ ' + events[1] +' <a href=' + events[4] +'><i class="icon-external-link"</i></a></li>');
        var infoWindow = new google.maps.InfoWindow({
          content: infoWindowContent
        });
        google.maps.event.addListener(marker, 'click', function() {
              infoWindow.open(map, marker);
        });
}

function codeAddress() {
    var address = document.getElementById("address").value;
    geocoder.geocode( { 'address': address}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
          map.setCenter(results[0].geometry.location);
          home = new google.maps.Marker({
            map: map,
            position: results[0].geometry.location
        });
    }
  });
}
//If the User is on a modern browser this will detect their location.
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(displayLocation);
}
//Get the user's current latitude and the longitude and assigns it to two variables. Then it calls the function codeLatLng and passes it the two variables as params.
function displayLocation(position) {
    var lat = position.coords.latitude;
    var lng = position.coords.longitude;
    codeLatLng(lat, lng);
}
//If LatLng is a valid address this fills the search bar with the most precise location availabe. Change the object retrieved in the Array to get a less precise address.
function codeLatLng(lat, lng) {
  var latlng = new google.maps.LatLng(lat, lng);
    geocoder.geocode({'latLng': latlng}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        console.log(results);
        if (results[1]) {
          $('#address').val(results[0].formatted_address);
         }
      }
   });
}
 
//This brings the map up and moves the searchbar and button to the bottom of the screen
     $('#map_canvas').css("visibility", "visible");
     $('#try_again').fadeIn(2000);



$('#list').toggle(function() {
  $('#try_again').animate({
      height: '100%'
    });
  
}, function() {
  $('#try_again').animate({
      height: '20%'
    });
});

//This allows the user to press enter to trigger the search
$("#address").keyup(function(event){
    if(event.keyCode == 13){
        $("#map_button").click();
    }
});

$(function() {
    $('#address').focus(function() {
      $(this).val('');
      });
 });
     $(function() {
    $('#map_button').click(function() {
    var searchAgain = $('#address').val();

   location.href = '?query=Boston';
      });
 });
