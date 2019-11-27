var redIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});


var n1 = [-34.1926,18.4456];
var n2 = [-34.1926,18.4456];
var n0 = [-34.1926,18.4456];
var trgt = [-34.181116,18.460078];
var map = L.map('map').setView([-34.19, 18.45], 13);
var target = L.marker(trgt,{icon: redIcon}).addTo(map);
var node0 = L.marker(n0).addTo(map);
var node1 = L.marker(n1).addTo(map);
var node2 = L.marker(n2).addTo(map);
var latlong = L.popup();
var polygon = L.polygon([
	n0,
	n1,
	trgt
]).addTo(map);
var polygon2 = L.polygon([
	n0,
	n2,
	trgt
]).addTo(map);
var b01 = L.polyline([n0, n1]).addTo(map);
var b02 = L.polyline([n0, n2]).addTo(map);


function onMapClick(e) {
	latlong
		.setLatLng(e.latlng)
		.setContent(e.latlng.toString())
		.openOn(map);
}

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
	attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
	maxZoom: 18,
    id: 'mapbox.outdoors',
	accessToken: 'pk.eyJ1IjoidXNlbmFtZXVzdXJwZXIiLCJhIjoiY2p6ZHdtMG9vMGJrNDNxdWl0OWJuZG9qeiJ9.YfrEsL3WyMm3aPG-kRXz1g'
}).addTo(map);

target.bindPopup("<b>Target</b><br>"+trgt).openPopup();
node0.bindPopup("<b>Node 0</b><br>"+n0).openPopup();
node1.bindPopup("<b>Node 1</b><br>"+n1).openPopup();
node2.bindPopup("<b>Node 2</b><br>"+n2).openPopup();
map.on('click', onMapClick);
