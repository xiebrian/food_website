
var map;
function initMapUSA() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 38.5, lng: -98.35},
        zoom: 4
    });
    var geocoder = new google.maps.Geocoder();

    var addresses = ["Fremont, CA", "Boston, MA", "Chicago, IL"];
    for (i = 0; i < addresses.length; i++) {
        var address = addresses[i];
        geocoder.geocode({'address': address}, function(results, status) {
            if (status === 'OK') {
                var marker = new google.maps.Marker({
                    map: map,
                    position: results[0].geometry.location
                });
            } else {
                alert("Geocode was not successful for the following reason: " + status);
            }
        });
    }
}
