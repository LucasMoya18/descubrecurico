/* Filtrado de comunas por región en crear_empresa */
document.addEventListener('DOMContentLoaded', function() {
    const regionSelect = document.getElementById('id_socio_region');
    const comunaSelect = document.getElementById('id_socio_comuna');
    
    if (!regionSelect || !comunaSelect) return;

    // Almacenar las comunas originales con sus regiones asociadas
    const comunasData = {};
    const allOptions = [];
    const options = comunaSelect.querySelectorAll('option');
    
    options.forEach(option => {
        if (option.value) {
            const regionId = option.getAttribute('data-region-id');
            allOptions.push({
                value: option.value,
                text: option.text,
                regionId: regionId
            });
            
            if (regionId) {
                if (!comunasData[regionId]) {
                    comunasData[regionId] = [];
                }
                comunasData[regionId].push({
                    value: option.value,
                    text: option.text
                });
            }
        }
    });

    // Función para filtrar comunas
    function filtrarComunas() {
        const selectedRegionId = regionSelect.value;
        
        // Limpiar todas las opciones excepto la vacía
        while (comunaSelect.options.length > 1) {
            comunaSelect.remove(1);
        }

        // Si no hay región seleccionada, mostrar todas las comunas
        if (!selectedRegionId) {
            allOptions.forEach(option => {
                const newOption = document.createElement('option');
                newOption.value = option.value;
                newOption.text = option.text;
                newOption.setAttribute('data-region-id', option.regionId);
                comunaSelect.appendChild(newOption);
            });
        } else {
            // Mostrar solo las comunas de la región seleccionada
            if (comunasData[selectedRegionId]) {
                comunasData[selectedRegionId].forEach(comuna => {
                    const newOption = document.createElement('option');
                    newOption.value = comuna.value;
                    newOption.text = comuna.text;
                    comunaSelect.appendChild(newOption);
                });
            }
        }

        // Resetear la selección de comuna
        comunaSelect.value = '';
    }

    // Escuchar cambios en región
    regionSelect.addEventListener('change', filtrarComunas);

    // Ejecutar filtrado inicial
    filtrarComunas();
});
