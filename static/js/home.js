$(document).ready(function() {
	var mapOptions = {
  		center: new google.maps.LatLng(-34.397, 150.644),
  		zoom: 4,
  		mapTypeId: google.maps.MapTypeId.ROADMAP
	};

	var map = new google.maps.Map(document.getElementById("home-map"), mapOptions);
});