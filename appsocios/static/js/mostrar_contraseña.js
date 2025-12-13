// Script para mostrar/ocultar contraseña con ícono de ojo

document.addEventListener('DOMContentLoaded', function() {
    // Encontrar todos los campos de contraseña
    const passwordFields = document.querySelectorAll('input[type="password"]');
    
    passwordFields.forEach(function(field) {
        // Crear contenedor para el campo y el ojo
        const container = document.createElement('div');
        container.style.position = 'relative';
        container.style.width = '100%';
        
        // Insertar el contenedor antes del campo
        field.parentNode.insertBefore(container, field);
        
        // Mover el campo dentro del contenedor
        container.appendChild(field);
        
        // Crear botón para mostrar/ocultar
        const toggleBtn = document.createElement('button');
        toggleBtn.type = 'button';
        toggleBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>';
        toggleBtn.style.position = 'absolute';
        toggleBtn.style.right = '12px';
        toggleBtn.style.top = '50%';
        toggleBtn.style.transform = 'translateY(-50%)';
        toggleBtn.style.background = 'none';
        toggleBtn.style.border = 'none';
        toggleBtn.style.cursor = 'pointer';
        toggleBtn.style.color = '#666';
        toggleBtn.style.display = 'flex';
        toggleBtn.style.alignItems = 'center';
        toggleBtn.style.padding = '8px';
        toggleBtn.style.zIndex = '10';
        toggleBtn.className = 'toggle-password-btn';
        
        container.appendChild(toggleBtn);
        
        // Evento para mostrar/ocultar
        toggleBtn.addEventListener('click', function(e) {
            e.preventDefault();
            if (field.type === 'password') {
                field.type = 'text';
                toggleBtn.style.color = '#1aabb6';
            } else {
                field.type = 'password';
                toggleBtn.style.color = '#666';
            }
        });
        
        // Agregar padding derecho al campo para que el ojo no lo tape
        field.style.paddingRight = '40px';
    });
});
