// Coordenadas de las ciudades principales de Chile por región
const coordenadasRegiones = {
    '1': { lat: -19.4, lng: -70.13, zoom: 11, nombre: 'Arica y Parinacota' },
    '2': { lat: -20.28, lng: -70.14, zoom: 11, nombre: 'Tarapacá' },
    '3': { lat: -22.9, lng: -68.19, zoom: 11, nombre: 'Antofagasta' },
    '4': { lat: -27.37, lng: -70.54, zoom: 11, nombre: 'Atacama' },
    '5': { lat: -29.9, lng: -71.25, zoom: 11, nombre: 'Coquimbo' },
    '6': { lat: -32.89, lng: -71.31, zoom: 11, nombre: 'Valparaíso' },
    '7': { lat: -33.45, lng: -70.67, zoom: 11, nombre: 'Metropolitana de Santiago' },
    '8': { lat: -34.17, lng: -71.04, zoom: 11, nombre: 'Libertador General Bernardo O\'Higgins' },
    '9': { lat: -35.43, lng: -71.55, zoom: 11, nombre: 'Maule' },
    '10': { lat: -36.6, lng: -72.1, zoom: 11, nombre: 'Ñuble' },
    '11': { lat: -37.27, lng: -73.16, zoom: 11, nombre: 'Biobío' },
    '12': { lat: -38.75, lng: -73.05, zoom: 11, nombre: 'La Araucanía' },
    '13': { lat: -39.8, lng: -73.25, zoom: 11, nombre: 'Los Ríos' },
    '14': { lat: -41.47, lng: -72.93, zoom: 11, nombre: 'Los Lagos' },
    '15': { lat: -43.62, lng: -73.6, zoom: 11, nombre: 'Aysén del General Carlos Ibáñez del Campo' },
    '16': { lat: -53.64, lng: -70.9, zoom: 11, nombre: 'Magallanes y de la Antártica Chilena' }
};

let mapa;
let marcador;

function inicializarMapa() {
    const regionId = document.getElementById('id_socio_region').value;
    
    if (!regionId || !coordenadasRegiones[regionId]) {
        alert('Por favor selecciona una región primero');
        return;
    }

    const coords = coordenadasRegiones[regionId];

    if (!mapa) {
        mapa = L.map('mapa').setView([coords.lat, coords.lng], coords.zoom);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(mapa);

        mapa.on('click', function(e) {
            const lat = e.latlng.lat;
            const lng = e.latlng.lng;
            mostrarMarcador(lat, lng);
            document.getElementById('info-lat').textContent = lat.toFixed(6);
            document.getElementById('info-lng').textContent = lng.toFixed(6);
        });
    } else {
        mapa.setView([coords.lat, coords.lng], coords.zoom);
    }
}

function mostrarMarcador(lat, lng) {
    if (marcador) {
        mapa.removeLayer(marcador);
    }
    
    marcador = L.marker([lat, lng]).addTo(mapa);
}

// Event listeners para los botones del modal
document.getElementById('btn-abrir-mapa').addEventListener('click', function() {
    const regionId = document.getElementById('id_socio_region').value;
    const comunaId = document.getElementById('id_socio_comuna').value;
    
    if (!regionId) {
        alert('Debe seleccionar una región primero');
        return;
    }
    
    
    
    document.getElementById('modal-mapa').style.display = 'flex';
    setTimeout(() => inicializarMapa(), 100);
});

document.getElementById('btn-cerrar-mapa').addEventListener('click', function() {
    document.getElementById('modal-mapa').style.display = 'none';
});

document.getElementById('btn-cancelar-mapa').addEventListener('click', function() {
    document.getElementById('modal-mapa').style.display = 'none';
});

document.getElementById('btn-guardar-ubicacion').addEventListener('click', function() {
    if (!marcador) {
        alert('Por favor selecciona un punto en el mapa');
        return;
    }
    
    const lat = marcador.getLatLng().lat;
    const lng = marcador.getLatLng().lng;
    
    document.getElementById('id_latitud').value = lat.toFixed(6);
    document.getElementById('id_longitud').value = lng.toFixed(6);
    
    document.getElementById('modal-mapa').style.display = 'none';
});

// Cerrar modal al hacer clic en el overlay
document.getElementById('modal-mapa').addEventListener('click', function(e) {
    if (e.target === this) {
        this.style.display = 'none';
    }
});
