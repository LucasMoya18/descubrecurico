document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contactForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            const btn = form.querySelector('button[type="submit"]');
            if (btn) {
                btn.disabled = true;
                btn.innerHTML = '<span class="inline-block animate-spin mr-2">↻</span> Enviando...';
                if (window.lucide) lucide.createIcons();
            }
        });
    }
});