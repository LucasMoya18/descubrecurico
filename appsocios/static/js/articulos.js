// ===============================
// DATOS DE LOS ARTÍCULOS
// ===============================
const articles = [
    {
        id: 1,
        title: "Parque Cuenca Andina: el corazón nativo del Maule abre sus puertas al mundo",
        excerpt: "En el corazón de la cordillera maulina, donde el viento conversa con los bosques nativos...",
        fullContent:
            "En el corazón de la cordillera maulina, donde el viento conversa con los bosques nativos, el Parque Cuenca Andina se consolida como un espacio de conservación y turismo sustentable.",
        image: "/static/imagenes/mountain-landscape-andes-chile.jpg",
        author: "Descubre Curicó",
        date: "Oct 4, 2025",
        category: "Cultura y Tradiciones",
        comments: [],
    },
    {
        id: 2,
        title: "Un nuevo hito en Descubre Curicó en sus 10 años",
        excerpt: "En la ciudad de Curicó, el día 22 de agosto de 2025, se llevó a cabo una reunión de networking...",
        fullContent:
            "El día 22 de agosto de 2025 se celebró una reunión de networking con emprendedores locales en honor a los 10 años de Descubre Curicó.",
        image: "/static/imagenes/business-meeting-group-photo.jpg",
        author: "Descubre Curicó",
        date: "Ago 24, 2025",
        category: "Noticias",
        comments: [],
    },
    {
        id: 3,
        title: "La ruta del vino: tradición, sabores y paisaje maulino",
        excerpt: "Entre viñedos centenarios y aromas frutales, la ruta del vino en Curicó se renueva...",
        fullContent:
            "Entre viñedos centenarios y aromas frutales, la ruta del vino en Curicó se renueva con propuestas enoturísticas que integran gastronomía local y experiencias sensoriales.",
        image: "/static/imagenes/wine-route-curico.jpg",
        author: "Descubre Curicó",
        date: "Sep 12, 2025",
        category: "Turismo",
        comments: [],
    },
    {
        id: 4,
        title: "Curicó Verde: iniciativas que transforman la ciudad",
        excerpt: "Nuevos proyectos urbanos impulsan una Curicó más sustentable y conectada con la naturaleza...",
        fullContent:
            "Curicó Verde promueve huertos comunitarios y espacios urbanos verdes para una ciudad más sustentable.",
        image: "/static/imagenes/green-city-curico.jpg",
        author: "Equipo Editorial",
        date: "Oct 10, 2025",
        category: "Sustentabilidad",
        comments: [],
    },
];

// ===============================
// PAGINACIÓN
// ===============================
let currentPage = 1;
const itemsPerPage = 4;

function renderArticles() {
    const totalPages = Math.ceil(articles.length / itemsPerPage);
    if (currentPage > totalPages) currentPage = totalPages;

    const start = (currentPage - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const visibleArticles = articles.slice(start, end);

    const container = document.getElementById("articlesContainer");
    container.innerHTML = visibleArticles
        .map(
            (article) => `
            <div class="rounded-2xl overflow-hidden bg-[var(--pure-white)] shadow-lg hover:shadow-[0_0_20px_var(--cyber-green)] transform hover:scale-[1.02] transition duration-300 text-[var(--storm-gray)]">
                <img src="${article.image}" alt="${article.title}" class="h-48 w-full object-cover opacity-90 hover:opacity-100 transition">
                <div class="p-5">
                    <h3 class="text-xl font-bold text-[var(--cyber-green)] mb-2">${article.title}</h3>
                    <p class="text-[var(--storm-gray)] text-sm mb-3 line-clamp-3">${article.excerpt}</p>
                    <div class="flex justify-between items-center text-xs text-[var(--storm-gray)]/70 mb-3">
                        <span>${article.date}</span>
                        <span>${article.category}</span>
                    </div>
                    <button onclick="openArticle(${article.id})" class="text-[var(--hot-magenta)] font-semibold hover:text-[var(--electric-violet)] transition">Leer más →</button>
                </div>
            </div>`
        )
        .join("");

    renderPagination(totalPages);
    if (typeof lucide !== "undefined") lucide.createIcons();
}

function renderPagination(totalPages) {
    const pageNumbers = document.getElementById("pageNumbers");
    pageNumbers.innerHTML = "";

    for (let i = 1; i <= totalPages; i++) {
        const btn = document.createElement("button");
        btn.textContent = i;
        btn.className = `px-3 py-1 rounded-lg border text-sm transition duration-200 font-medium ${
            i === currentPage
                ? "bg-[var(--cyber-green)] text-[var(--pure-white)] border-[var(--cyber-green)]"
                : "text-[var(--cyber-green)] border-[var(--cyber-green)] hover:bg-[var(--cyber-green)] hover:text-[var(--pure-white)]"
        }`;
        btn.onclick = () => {
            currentPage = i;
            renderArticles();
        };
        pageNumbers.appendChild(btn);
    }

    const prevButton = document.getElementById("prevPage");
    const nextButton = document.getElementById("nextPage");
    if (prevButton) prevButton.disabled = currentPage === 1;
    if (nextButton) nextButton.disabled = currentPage === totalPages;
}

// ===============================
// MODAL DE ARTÍCULO + COMENTARIOS
// ===============================
function openArticle(id) {
    const article = articles.find((a) => a.id === id);
    const modal = document.getElementById("articleModal");
    const modalContent = document.getElementById("modalContent");
    const label = document.getElementById("articleModalLabel");

    label.textContent = article.title;
    modalContent.innerHTML = `
        <div class="space-y-6 overflow-y-auto max-h-[75vh] pr-4 text-[var(--storm-gray)]">
            <img src="${article.image}" alt="${article.title}" class="w-full h-64 object-cover rounded-xl">
            <p class="text-sm text-[var(--storm-gray)]/80">${article.date} — ${article.author}</p>
            <p class="leading-relaxed">${article.fullContent}</p>

            <hr class="border-[var(--storm-gray)]/40 my-4">

            <!-- Formulario de comentarios -->
            <h4 class="text-lg font-bold text-[var(--cyber-green)]">💬 Deja un comentario</h4>
            <div class="space-y-3">
                <input id="name-${article.id}" type="text" placeholder="Tu nombre" class="w-full px-3 py-2 rounded-lg bg-[var(--pure-white)] text-[var(--storm-gray)] placeholder-[var(--storm-gray)]/50 border border-[var(--storm-gray)]/30 focus:outline-none focus:ring-2 focus:ring-[var(--cyber-green)]">
                <input id="email-${article.id}" type="email" placeholder="Tu correo electrónico" class="w-full px-3 py-2 rounded-lg bg-[var(--pure-white)] text-[var(--storm-gray)] placeholder-[var(--storm-gray)]/50 border border-[var(--storm-gray)]/30 focus:outline-none focus:ring-2 focus:ring-[var(--cyber-green)]">
                <textarea id="comment-${article.id}" placeholder="Escribe tu comentario..." rows="3" class="w-full px-3 py-2 rounded-lg bg-[var(--pure-white)] text-[var(--storm-gray)] placeholder-[var(--storm-gray)]/50 border border-[var(--storm-gray)]/30 focus:outline-none focus:ring-2 focus:ring-[var(--cyber-green)]"></textarea>
                <button onclick="addComment(${article.id})" class="px-4 py-2 rounded-lg bg-[var(--hot-magenta)] hover:bg-[var(--electric-violet)] text-white font-semibold transition">Enviar</button>
            </div>

            <!-- Comentarios -->
            <div id="comments-${article.id}" class="mt-6 space-y-3">
                ${
                    article.comments.length > 0
                        ? article.comments
                              .map(
                                  (c) => `
                        <div class="bg-[var(--pure-white)] rounded-lg p-3 border border-[var(--storm-gray)]/30 text-[var(--storm-gray)]">
                            <p class="text-sm"><strong>${c.name}</strong> — <span class="text-[var(--storm-gray)]/70">${c.email}</span></p>
                            <p class="mt-1">${c.text}</p>
                        </div>`
                              )
                              .join("")
                        : `<p class="text-sm text-[var(--storm-gray)]/70">Aún no hay comentarios. ¡Sé el primero!</p>`
                }
            </div>
        </div>
    `;

    modal.classList.remove("hidden");
    if (typeof lucide !== "undefined") lucide.createIcons();
}

function addComment(id) {
    const name = document.getElementById(`name-${id}`).value.trim();
    const email = document.getElementById(`email-${id}`).value.trim();
    const text = document.getElementById(`comment-${id}`).value.trim();

    if (!name || !email || !text) {
        alert("Por favor, completa todos los campos.");
        return;
    }

    const article = articles.find((a) => a.id === id);
    article.comments.push({ name, email, text });

    openArticle(id);
}

document.getElementById("closeModal").onclick = () => {
    document.getElementById("articleModal").classList.add("hidden");
};

// ===============================
// INICIALIZACIÓN
// ===============================
document.addEventListener("DOMContentLoaded", () => {
    const prevButton = document.getElementById("prevPage");
    const nextButton = document.getElementById("nextPage");

    if (prevButton) {
        prevButton.onclick = () => {
            if (currentPage > 1) {
                currentPage--;
                renderArticles();
            }
        };
    }

    if (nextButton) {
        nextButton.onclick = () => {
            const totalPages = Math.ceil(articles.length / itemsPerPage);
            if (currentPage < totalPages) {
                currentPage++;
                renderArticles();
            }
        };
    }

    renderArticles();
});
