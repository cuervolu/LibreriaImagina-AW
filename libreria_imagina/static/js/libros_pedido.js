$(document).ready(function () {
    // Cuando se seleccione una opción en el combo box de pedidos
    $('#misPedidos').on('change', function () {
      var selectedPedidoId = $(this).val(); // Obtener el ID del pedido seleccionado
      var comboLibro = $('#libro');
      if (selectedPedidoId) {
        // Habilitar el combo box de libros
        comboLibro.prop('disabled', false);
        // Realizar una solicitud AJAX para obtener los libros del pedido seleccionado
        $.ajax({
          url: '/obtener_libros/',
          data: { pedido_id: selectedPedidoId },
          success: function (response) {
            // Vaciar el combo box de libros
            comboLibro.empty();
            // Agregar la opción "Selecciona un libro" al principio
            comboLibro.append($('<option>').val('').text('Seleccione un libro'));
            // Agregar las opciones de libros del pedido
            $.each(response.libros, function (index, libro) {
                var option = $('<option>')
                  .val(libro.id_libro)
                  .text(libro.nombre_libro)
                  .data('thumbnail', libro.thumbnail);
                comboLibro.append(option);
            });
          }
        });
        $('#imagenLibroContainer').hide();
        imagenLibro.attr('src', '');
      } else {
        // Vaciar el combo box de libros
        comboLibro.empty();
        // Agregar la opción "Selecciona un libro" al principio
        comboLibro.append($('<option>').val('').text('Seleccione un libro'));
        // Deshabilitar el combo box de libros, excepto cuando se selecciona la opción por defecto
        if ($(this).find('option:selected').index() !== '') {
          comboLibro.prop('disabled', true);
          $('#imagenLibroContainer').hide();
          imagenLibro.attr('src', '');
        }
      }
    });
  
    // Deshabilitar el combo box de libros al cargar la página si la opción por defecto está seleccionada
    if ($('#misPedidos option:selected').index() === 0) {
      $('#libro').prop('disabled', true);
    }

    $('#libro').on('change', function () {
        var selectedLibroId = $(this).val(); // Obtener el ID del libro seleccionado
    
        // Obtener el elemento de la imagen del libro
        var imagenLibro = $('#imagenLibro');
    
        if (selectedLibroId) {
          // Obtener la URL de la imagen del libro desde el atributo "thumbnail"
          var selectedLibroThumbnail = $(this).find(':selected').data('thumbnail');
    
          // Asignar la URL de la imagen al atributo "src" de la etiqueta <img>
          imagenLibro.attr('src', selectedLibroThumbnail);
    
          // Mostrar el contenedor y la imagen del libro
          $('#imagenLibroContainer').show();
        } else {
          // Si no se selecciona ningún libro, ocultar el contenedor y la imagen
          $('#imagenLibroContainer').hide();
          imagenLibro.attr('src', '');
        }
      });
  });
  