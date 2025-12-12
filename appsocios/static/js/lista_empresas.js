/* global lucide, L */

const lucide = window.lucide

// Elementos del DOM
const modalMapa = document.getElementById("modalMapa")
const cerrarModal = document.getElementById("cerrarModal")
const cerrarModalBtn = document.getElementById("cerrarModalBtn")
const mapa = document.getElementById("mapa")
const modalTitle = document.getElementById("modalTitle")
const modalDireccion = document.getElementById("modalDireccion")
const modalCoordenadas = document.getElementById("modalCoordenadas")

let mapaInstancia = null
let activeRubro = ''

// Cargar eventos al DOM listo
document.addEventListener("DOMContentLoaded", () => {
  setupEventListeners()
  setupFiltros()
  setupGridControls()
  if (lucide) lucide.createIcons()
})

function setupEventListeners() {
  // Botones "Cómo llegar"
  document.querySelectorAll(".como-llegar-btn").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault()
      const nombre = btn.dataset.nombre
      const direccion = btn.dataset.direccion
      const lat = parseFloat(btn.dataset.lat)
      const lng = parseFloat(btn.dataset.lng)

      abrirModalMapa(nombre, direccion, lat, lng)
    })
  })

  // Cerrar modal (botón X)
  if (cerrarModal) {
    cerrarModal.addEventListener("click", () => {
      cerrarModalMapa()
    })
  }

  // Cerrar modal (botón Cerrar)
  if (cerrarModalBtn) {
    cerrarModalBtn.addEventListener("click", () => {
      cerrarModalMapa()
    })
  }

  // Cerrar modal al hacer clic en el overlay
  if (modalMapa) {
    modalMapa.addEventListener("click", (e) => {
      if (e.target === modalMapa) {
        cerrarModalMapa()
      }
    })
  }
}

function abrirModalMapa(nombre, direccion, lat, lng) {
  modalTitle.textContent = nombre
  modalDireccion.textContent = direccion
  modalCoordenadas.textContent = `${lat.toFixed(4)}, ${lng.toFixed(4)}`

  modalMapa.classList.remove("hidden")

  // Limpiar mapa anterior si existe
  if (mapaInstancia) {
    mapaInstancia.remove()
    mapaInstancia = null
  }

  // Crear nuevo mapa
  setTimeout(() => {
    if (typeof L === "undefined") {
      mapa.innerHTML = '<p class="text-red-600 text-center p-4">Error: Leaflet no cargó correctamente</p>'
      return
    }

    mapaInstancia = L.map("mapa", { scrollWheelZoom: false }).setView([lat, lng], 15)

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: "&copy; OpenStreetMap contributors",
    }).addTo(mapaInstancia)

    // Agregar marcador
    L.marker([lat, lng])
      .addTo(mapaInstancia)
      .bindPopup(`<strong>${nombre}</strong><br>${direccion}`)
      .openPopup()
  }, 300)
}

function cerrarModalMapa() {
  modalMapa.classList.add("hidden")
  if (mapaInstancia) {
    mapaInstancia.remove()
    mapaInstancia = null
  }
}

/* ------------------ GRID CONTROLS (2/3/4) ------------------ */
function setupGridControls() {
  const gridBtns = document.querySelectorAll('.grid-btn')
  const grid = document.getElementById('empresasGrid')
  if (!grid || gridBtns.length === 0) return

  // aplicar valor guardado (default 4)
  const saved = localStorage.getItem('empresas_cols') || '4'
  applyGrid(saved)

  // marcar botón activo por defecto
  gridBtns.forEach(b => b.classList.remove('bg-vine-green','text-white'))
  const activeBtn = Array.from(gridBtns).find(b => b.dataset.cols === saved)
  if (activeBtn) activeBtn.classList.add('bg-vine-green','text-white')

  gridBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const cols = btn.dataset.cols
      applyGrid(cols)
      gridBtns.forEach(b => b.classList.remove('bg-vine-green','text-white'))
      btn.classList.add('bg-vine-green','text-white')
      localStorage.setItem('empresas_cols', cols)
    })
  })
}

function applyGrid(cols) {
  const grid = document.getElementById('empresasGrid')
  if (!grid) return
  grid.classList.remove('cols-2','cols-3','cols-4')
  const cls = `cols-${cols}`
  grid.classList.add(cls)
}

/* ------------------ FILTRADO (BUSCAR + RUBROS) ------------------ */
function setupFiltros() {
  const buscarInput = document.getElementById('buscarEmpresa')
  const rubroBtns = document.querySelectorAll('.rubro-btn')

  if (buscarInput) {
    buscarInput.addEventListener('input', () => {
      filterEmpresas()
    })
  }

  rubroBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      // Toggle active
      rubroBtns.forEach(b => b.classList.remove('bg-vine-green', 'text-white'))
      btn.classList.add('bg-vine-green', 'text-white')
      activeRubro = btn.dataset.rubroId || ''
      filterEmpresas()
    })
  })
}

function filterEmpresas() {
  const query = (document.getElementById('buscarEmpresa')?.value || '').toLowerCase().trim()
  const items = document.querySelectorAll('.business-item')

  items.forEach(item => {
    const nombre = (item.querySelector('h3')?.textContent || '').toLowerCase()
    const rubroId = (item.dataset.rubroId || '') + ''

    const matchName = !query || nombre.includes(query)
    const matchRubro = !activeRubro || rubroId === activeRubro

    if (matchName && matchRubro) {
      item.style.display = ''
    } else {
      item.style.display = 'none'
    }
  })
}

/* Fin */
