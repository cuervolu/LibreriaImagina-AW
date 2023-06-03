$(document).ready(function () {
    // Cuando se seleccione una opción en el select de regiones
    $('#regionSelect').on('change', function () {
        var selectedRegionId = $(this).val(); // Obtener el ID de la región seleccionada
        var comunaSelect = $('#comunaSelect');
        if (selectedRegionId) {
            // Habilitar el select de comunas
            comunaSelect.prop('disabled', false);
            // Realizar una solicitud AJAX para obtener las comunas filtradas
            $.ajax({
                url: '/obtener_comunas/',
                data: { region_id: selectedRegionId },
                success: function (response) {
                    // Vaciar el select de comunas
                    comunaSelect.empty();
                    // Agregar las opciones de comunas filtradas
                    $.each(response.comunas, function (index, comuna) {
                        var option = $('<option>').val(comuna.id_comuna).text(comuna.nombre_comuna);
                        comunaSelect.append(option);
                    });
                }
            });
        } else {
            // Vaciar el select de comunas
            comunaSelect.empty();
            // Deshabilitar el select de comunas, excepto cuando se selecciona la opción por defecto
            if ($(this).find('option:selected').index() !== 0) {
                comunaSelect.prop('disabled', true);
            }
        }
    });

    // Deshabilitar el select de comunas al cargar la página si la opción por defecto está seleccionada
    if ($('#regionSelect option:selected').index() === 0) {
        $('#comunaSelect').prop('disabled', true);
    }
});