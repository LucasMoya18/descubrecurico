/* global lucide */

// Empresas / negocios (datos mock)
// Lista de objetos que representan negocios. Cada línea tiene un comentario breve.
const businesses = [
  {
    id: 1, // identificador único del negocio
    name: "Hotel Boutique Raíces", // nombre mostrado
    category: "Alojamiento", // categoría del negocio
    phone: "(+56) 75 2 543440", // teléfono de contacto
    email: "recepcion@hotelraices.cl", // email de contacto
    address: "Carmen 727, Curicó", // dirección fiscal/visible
    image: "/static/imagenes/boutique-hotel-chile.jpg", // ruta de la imagen
    featured: false, // indica si aparece como destacado
    lat: -34.9825,lon: -71.2394, // latitud y longitud (en la misma línea)
  },
  {
    id: 2, // id único
    name: "Maule Norte GLP", // nombre
    category: "Venta de productos", // categoria
    phone: "+56978748999", // teléfono
    email: "luismoralescastro@hotmail.com", // email
    address: "Callejón Hijuelas S/N Santa Helena", // dirección
    image: "/static/imagenes/gas-distribution-company.jpg", // imagen
    featured: false, // destacado?
    lat: -35.022, lon: -71.200 // coordenadas
  },
  {
    id: 3, // id único
    name: "Miqueles Boutique", // nombre
    category: "Venta de productos", // categoria
    phone: "+56949685316", // teléfono
    email: "amandamiqueles@gmail.com", // email
    address: "O'Higgins 487, Curicó", // dirección
    image: "/static/imagenes/fashion-boutique.png", // imagen
    featured: true, // marcado como destacado
    lat: -35.035, lon: -71.230 // coordenadas
  },
  {
    id: 4, // id
    name: "Play Solution", // nombre
    category: "Servicios", // categoria
    phone: "+56912345678", // telefono
    email: "contacto@playsolution.cl", // email
    address: "Av. Manso de Velasco 1234, Curicó", // direccion
    image: "/static/imagenes/team-building-activities.png", // imagen
    featured: true, // destacado
    lat: -34.970, lon: -71.245 // coordenadas
  },
  {
    id: 5, // id
    name: "Gestor Consultoría", // nombre
    category: "Servicios", // categoria
    phone: "+56987654321", // telefono
    email: "info@gestorconsultoria.cl", // email
    address: "Merced 567, Curicó", // direccion
    image: "/static/imagenes/business-consulting-office.png", // imagen
    featured: true, // destacado
    lat: -34.990, lon: -71.220 // coordenadas
  },
  {
    id: 6, // id
    name: "Renace Mujer", // nombre
    category: "Servicios", // categoria
    phone: "+56923456789", // telefono
    email: "contacto@renacemujer.cl", // email
    address: "Carmen 890, Curicó", // direccion
    image: "/static/imagenes/women-empowerment-center.jpg", // imagen
    featured: true, // destacado
    lat: -35.000, lon: -71.210 // coordenadas
  },
]

// State
let currentCategory = "Todas" // categoría actualmente seleccionada (filtro)
let searchQuery = "" // texto de búsqueda actual
let map = null // referencia al mapa Leaflet una vez inicializado
let markers = [] // array con marcadores actuales en el mapa
let markerById = {} // mapeo { idNegocio: marcador }
let selectedBusinessId = null // id del negocio seleccionado

const lucide = window.lucide // referencia a lucide (icons)

// DOM elements
const gridView = document.getElementById("gridView") // contenedor de tarjetas
const mapView = document.getElementById("mapView") // contenedor del mapa
const noResults = document.getElementById("noResults") // mensaje sin resultados
const searchInput = document.getElementById("searchInput") // input de búsqueda
const resultsCount = document.getElementById("resultsCount") // contador de resultados
const gridViewBtn = document.getElementById("gridViewBtn") // botón vista en grilla
const mapViewBtn = document.getElementById("mapViewBtn") // botón vista mapa

// Espera a que el DOM esté cargado para inicializar
document.addEventListener("DOMContentLoaded", () => {
  setupEventListeners() // configurar listeners UI
  renderBusinesses() // renderizar lista inicial
  if (lucide) lucide.createIcons() // generar iconos si lucide está presente
})

function setupEventListeners() {
  // Search
  if (searchInput) {
    // cuando el usuario escribe, actualizamos el query y re-renderizamos
    searchInput.addEventListener("input", (e) => {
      searchQuery = e.target.value.toLowerCase() // guardar búsqueda en minúsculas
      renderBusinesses() // refrescar lista
    })
  }

  // Category buttons (live bind)
  // configuramos click en cada botón de categoría
  document.querySelectorAll(".category-btn").forEach((btn) => {
    btn.addEventListener("click", function () {
      // limpiar estilos de todos los botones
      document.querySelectorAll(".category-btn").forEach((b) => {
        b.classList.remove("active", "bg-harvest-gold", "text-burgundy-reserve")
        b.classList.add("bg-white", "text-burgundy-reserve", "border", "border-vine-green/40")
      })

      // aplicar estilos al botón actual
      this.classList.add("active", "bg-harvest-gold", "text-burgundy-reserve")
      this.classList.remove("bg-white", "border", "border-vine-green/40")

      // actualizar categoría y re-renderizar
      currentCategory = this.dataset.category || "Todas"
      renderBusinesses()
    })
  })

  // View toggle
  if (gridViewBtn) {
    // mostrar la grilla al hacer click
    gridViewBtn.addEventListener("click", () => {
      gridView.classList.remove("hidden") // mostrar grilla
      mapView.classList.add("hidden") // ocultar mapa
      gridViewBtn.classList.add("bg-white", "text-burgundy-reserve") // estilo activo
      gridViewBtn.classList.remove("text-white")
      mapViewBtn.classList.remove("bg-white", "text-burgundy-reserve")
      mapViewBtn.classList.add("text-white")
    })
  }

  if (mapViewBtn) {
    // mostrar el mapa al hacer click
    mapViewBtn.addEventListener("click", () => {
      gridView.classList.add("hidden") // ocultar grilla
      mapView.classList.remove("hidden") // mostrar mapa
      mapViewBtn.classList.add("bg-white", "text-burgundy-reserve") // estilo activo
      mapViewBtn.classList.remove("text-white")
      gridViewBtn.classList.remove("bg-white", "text-burgundy-reserve")
      gridViewBtn.classList.add("text-white")

      // initialize map lazily si aún no existe
      if (!map) initMap()
      if (lucide) lucide.createIcons() // recrear iconos si es necesario
    })
  }
}

function filterBusinesses() {
  // devuelve la lista filtrada por búsqueda y categoría
  return businesses.filter((business) => {
    const matchesSearch =
      business.name.toLowerCase().includes(searchQuery) || business.address.toLowerCase().includes(searchQuery) // busca en nombre y dirección
    const matchesCategory = currentCategory === "Todas" || business.category === currentCategory // chequea categoría
    return matchesSearch && matchesCategory // se requiere cumplir ambas
  })
}

function renderBusinesses() {
  const filtered = filterBusinesses() // obtener lista filtrada
  document.getElementById("resultsCount").textContent = filtered.length // actualizar contador

  if (filtered.length === 0) {
    gridView.innerHTML = "" // limpiar grilla
    noResults.classList.remove("hidden") // mostrar mensaje "no results"
    if (map) updateMarkers([]) // limpiar marcadores si mapa existe
    if (lucide) lucide.createIcons() // generar iconos
    return // salir
  }

  noResults.classList.add("hidden") // ocultar mensaje de sin resultados

  // Construir el HTML de las tarjetas: usamos template literal para cada negocio
  gridView.innerHTML = filtered
    .map(
      (business) => `
        <div class="business-card bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden border border-gray-200" data-business-id="${business.id}">
            <div class="relative h-56 overflow-hidden p-4">
                <div class="relative h-full w-full">
                    <img src="${business.image}" 
                         alt="${business.name}" 
                         class="w-full h-full object-cover rounded-lg border-2 border-burgundy-reserve">
                </div>
            </div>
            <div class="p-6">
                <div class="flex items-center gap-2 mb-3">
                    <span class="px-3 py-1 bg-vine-green text-white text-xs rounded-full font-medium">
                        ${business.category}
                    </span>
                </div>
                <h3 class="text-xl font-bold text-burgundy-reserve mb-4">${business.name}</h3>
        <div class="space-y-2 text-sm text-slate-gray">
                    <div class="flex items-center gap-2">
                        <i data-lucide="phone" class="h-4 w-4 text-harvest-gold"></i>
                        <span>${business.phone}</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <i data-lucide="mail" class="h-4 w-4 text-harvest-gold"></i>
                        <span class="break-all">${business.email}</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <i data-lucide="map-pin" class="h-4 w-4 text-harvest-gold"></i>
                        <span>${business.address}</span>
                    </div>
                </div>
                
        <div class="mt-4">
          <button data-business-id="${business.id}" class="go-map-btn inline-flex items-center gap-2 px-4 py-2 rounded-md bg-[#6e0e0a] text-white hover:bg-[#4a0907] transition-colors">
            Cómo llegar
          </button>
        </div>
      </div>
        </div>
    `,
    )
    .join("") // unir todos los templates en un string

  if (lucide) lucide.createIcons() // generar iconos lucide para las tarjetas

  // Attach card click handlers so selecting a card opens popup / centers on map
  document.querySelectorAll('.business-card').forEach((card) => {
    const id = Number(card.dataset.businessId) // leer id desde el atributo
    card.addEventListener('click', () => selectBusiness(id)) // al click seleccionar negocio
  })

  // Attach "Cómo llegar" buttons to switch to map and center marker
  document.querySelectorAll('.go-map-btn').forEach((btn) => {
    const id = Number(btn.dataset.businessId) // id asociado al botón
    btn.addEventListener('click', (e) => {
      e.stopPropagation() // evitar que el click burbujee y dispare el handler de la tarjeta
      // switch view to map (mirror existing view toggle behavior)
      try {
        gridView.classList.add('hidden')
        mapView.classList.remove('hidden')
        mapViewBtn.classList.add('bg-white', 'text-burgundy-reserve')
        mapViewBtn.classList.remove('text-white')
        gridViewBtn.classList.remove('bg-white', 'text-burgundy-reserve')
        gridViewBtn.classList.add('text-white')
      } catch (err) {}

      // initialize map if not present, then select the business
      if (!map) {
        initMap() // crear mapa
        // selection after a short delay to allow map & markers to initialize
        setTimeout(() => {
          selectBusiness(id) // seleccionar marcador después de inicializar
        }, 700)
      } else {
        selectBusiness(id) // seleccionar marcador inmediatamente
      }
    })
  })

  // apply selected class if a business is selected
  syncCardSelection() // actualizar clases visuales de selección

  // update map markers if map exists
  if (map) updateMarkers(filtered) // refrescar marcadores según lista filtrada
}

function syncCardSelection() {
  // marca visualmente la tarjeta seleccionada y hace scroll si es necesario
  document.querySelectorAll('.business-card').forEach((card) => {
    const id = Number(card.dataset.businessId) // id de la tarjeta
    if (selectedBusinessId && id === selectedBusinessId) {
      card.classList.add('ring-4', 'ring-[#d4af37]/40') // aplicar anillo dorado
      // ensure visible: intentar hacer scroll hacia la tarjeta
      try { card.scrollIntoView({ behavior: 'smooth', block: 'center' }) } catch (e) {}
    } else {
      card.classList.remove('ring-4', 'ring-[#d4af37]/40') // remover estilo si no coincide
    }
  })
}

function selectBusiness(id) {
  // seleccionar un negocio por id; si ya está seleccionado, no hacer nada
  if (selectedBusinessId === id) return
  selectedBusinessId = id // actualizar estado
  syncCardSelection() // aplicar clases visuales

  // if marker exists, open popup and center
  const m = markerById[id] // obtener marcador por id
  if (map && m) {
    try {
      m.openPopup() // abrir popup del marcador
      const latlng = m.getLatLng() // coordenadas del marcador
      map.setView(latlng, 15, { animate: true }) // centrar mapa con zoom
    } catch (e) {
      try { map.panTo(m.getLatLng()) } catch (err) {} // fallback: panTo
    }
  }
}

function clearSelection() {
  // limpiar selección actual
  selectedBusinessId = null
  syncCardSelection() // actualizar UI
  if (map) map.closePopup() // cerrar popup si hay mapa
}

/* Map related helpers */
// Carga Leaflet (CSS + JS) de forma dinámica y llama callback cuando está listo
function loadLeaflet(callback) {
  if (window.L) return callback() // si ya está cargado, ejecutar callback

  // load css
  const link = document.createElement('link')
  link.rel = 'stylesheet' // rel stylesheet
  link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css' // url CSS
  document.head.appendChild(link) // añadir al head

  // load script
  const script = document.createElement('script')
  script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js' // url JS
  script.onload = () => callback() // cuando cargue, ejecutar callback
  document.body.appendChild(script) // añadir al body
}

// small helper to avoid XSS in popup content
function escapeHtml(str) {
  // convierte a string y reemplaza caracteres especiales por entidades
  return String(str || '').replace(/[&<>"]+/g, function (s) {
    return ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;'
    })[s]
  })
}

function initMap() {
  // cargar leaflet y, al estar listo, inicializar el mapa
  loadLeaflet(() => {
    // create map inside mapView
    // ensure mapView has an inner container with fixed height
    let mapContainer = document.getElementById('mapCanvas') // buscar contenedor ya existente
    if (!mapContainer) {
      mapContainer = document.createElement('div') // crear si no existe
      mapContainer.id = 'mapCanvas'
      mapContainer.style.width = '100%'
      mapContainer.style.height = '600px' // altura fija por defecto
      mapView.innerHTML = '' // limpiar contenido actual
      mapView.appendChild(mapContainer) // añadir canvas al DOM
    }

    map = L.map('mapCanvas', { scrollWheelZoom: false }) // crear instancia de mapa

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; OpenStreetMap contributors' // atribución requerida
    }).addTo(map)

    // add markers for current filtered list
    const initial = filterBusinesses() // obtener lista actual
    updateMarkers(initial) // dibujar marcadores
  })
}

function clearMarkers() {
  // eliminar todos los marcadores del mapa y resetear arrays
  if (!map) return // si no hay mapa, nada que hacer
  markers.forEach(m => map.removeLayer(m)) // remover cada marcador
  markers = [] // limpiar array
  markerById = {} // limpiar mapeo
}

function updateMarkers(list) {
  // actualizar marcadores en el mapa basado en la lista recibida
  if (!map) return // si no hay mapa, salir
  clearMarkers() // limpiar marcadores previos
  const points = [] // acumula coordenadas para fitBounds
  list.forEach(b => {
    if (typeof b.lat !== 'number' || typeof b.lon !== 'number') return // validar coords
    const marker = L.marker([b.lat, b.lon]).addTo(map) // crear y añadir marcador
    const popup = `<strong>${escapeHtml(b.name)}</strong><br>${escapeHtml(b.address)}<br><small>${escapeHtml(b.phone || '')}</small>` // contenido seguro del popup
    marker.bindPopup(popup) // enlazar popup al marcador
    // when marker clicked, select the business and open popup (will already open)
    marker.on('click', () => selectBusiness(b.id)) // seleccionar negocio al click en marcador
    markers.push(marker) // almacenar marcador
    markerById[b.id] = marker // mapear por id
    points.push([b.lat, b.lon]) // añadir punto para bounds
  })

  if (points.length === 0) {
    map.setView([-35.0, -71.2], 12) // vista por defecto si no hay puntos
  } else if (points.length === 1) {
    map.setView(points[0], 14) // centrar en punto único
  } else {
    const bounds = L.latLngBounds(points) // calcular bounds
    map.fitBounds(bounds.pad(0.2)) // ajustar vista con padding
  }
}

