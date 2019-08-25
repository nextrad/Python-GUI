var map = L.map('map').setView([-34.19, 18.45], 13);
var target = L.marker([-34.181073, 18.460132]).addTo(map);
var node0 = L.marker([-34.165511, 18.43214]).addTo(map);
var node1 = L.marker([-34.192475, 18.445689]).addTo(map);
var node2 = L.marker([-34.1925, 18.445689]).addTo(map);
var latlong = L.popup();
var polygon = L.polygon([
	[-34.192475, 18.445689],
	[-34.17105, 18.457117],
	[-34.180779, 18.471622]
]).addTo(map);


function onMapClick(e) {
	latlong
		.setLatLng(e.latlng)
		.setContent(e.latlng.toString())
		.openOn(map);
}

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
	attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
	maxZoom: 18,
	id: 'mapbox.streets',
	accessToken: 'pk.eyJ1IjoidXNlbmFtZXVzdXJwZXIiLCJhIjoiY2p6ZHdtMG9vMGJrNDNxdWl0OWJuZG9qeiJ9.YfrEsL3WyMm3aPG-kRXz1g'
}).addTo(map);
target.bindPopup("<b>Target</b><br>Roman Rock").openPopup();
node0.bindPopup("<b>Node0</b><br>Elsies Bay").openPopup();
node1.bindPopup("<b>Node1</b><br>IMT").openPopup();
node2.bindPopup("<b>Node2</b><br>IMT").openPopup();
map.on('click', onMapClick);