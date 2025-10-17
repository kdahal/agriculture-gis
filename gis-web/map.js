// Initialize map centered on farm (example coords)
var map = L.map('map').setView([40.7128, -74.0060], 13);  // Replace with farm lat/lng
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
}).addTo(map);  // Added trailing comma to options object

// Drone markers array
var drones = L.layerGroup().addTo(map);

// Simulate or receive real-time GPS updates via WebSocket/UDP proxy
function updateDronePositions(data) {
    data.forEach(function(drone) {
        var marker = L.marker([drone.lat, drone.lng]).bindPopup(drone.id);
        drones.clearLayers().addLayer(marker);  // Update positions
    });
}

// Example: Poll for data every 5s (replace with real mesh data feed)
setInterval(function() {
    // Fetch from backend API aggregating mesh GPS
    fetch('/api/drones').then(res => res.json()).then(updateDronePositions);
}, 5000);