function confirmDeleteCartProduct(detalle_carrito_id){
    Swal.fire({
        title: 'Estas seguro?',
        text: "No podrás deshacer la acción!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si, borralo!',
        cancelButtonText: "Cancelar"
      }).then((result) => {
        if (result.isConfirmed) {
          Swal.fire(
            'Eliminado!',
            'Producto eliminado correctamente.',
            'success'
          ).then(function() {
            window.location.href = "cart/eliminar/"+ detalle_carrito_id +"/";
          })
        }
      })
}


function confirmAddNewAddress(event) {
    event.preventDefault(); // Prevenir comportamiento predeterminado del botón

    var form = document.getElementById("myFormAdrresses");

    // Validar los datos del formulario
    if (form.checkValidity()) {
        // Los datos son válidos, mostrar SweetAlert
        Swal.fire({
            title: '¿Estás seguro?',
            text: "¡No podrás deshacer esta acción!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí, agregar domicilio!',
            cancelButtonText: 'Cancelar'
        }).then(function (result) {
            if (result.isConfirmed) {
                Swal.fire(
                    'Agregado!',
                    'Domicilio agregado correctamente.',
                    'success'
                ).then(function () {
                    form.submit(); // Enviar el formulario manualmente
                });
            }
        });
    } else {
        // Los datos no son válidos, realizar alguna acción (mostrar mensaje de error, etc.)
        alert("Por favor, completa todos los campos requeridos correctamente.");
    }
}

function confirmDeleteAddress(event){
    event.preventDefault(); // Prevenir comportamiento predeterminado del botón

    var form = document.getElementById("formDeleteAddress");
    Swal.fire({
        title: 'Estas seguro?',
        text: "No podrás deshacer la acción!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si, borralo!',
        cancelButtonText: "Cancelar"
      }).then((result) => {
        if (result.isConfirmed) {
          Swal.fire(
            'Eliminado!',
            'Domicilio eliminado correctamente.',
            'success'
          ).then(function () {
            form.submit(); // Enviar el formulario manualmente
        });
        }
      })
}

function confirmAddCreditCard(event) {
    event.preventDefault(); // Prevenir comportamiento predeterminado del botón

    var form = document.getElementById("myFormCards");

    // Validar los datos del formulario
    if (form.checkValidity()) {
        // Los datos son válidos, mostrar SweetAlert
        Swal.fire({
            title: '¿Estás seguro?',
            text: "¡Agregarás una nueva tarjeta!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí, agregar tarjeta!',
            cancelButtonText: 'Cancelar'
        }).then(function (result) {
            if (result.isConfirmed) {
                Swal.fire(
                    'Agregado!',
                    'Tarjeta agregada correctamente.',
                    'success'
                ).then(function () {
                    form.submit(); // Enviar el formulario manualmente
                });
            }
        });
    } else {
        // Los datos no son válidos, realizar alguna acción (mostrar mensaje de error, etc.)
        alert("Por favor, completa todos los campos requeridos correctamente.");
    }
}

function confirmDeleteCreditCard(event){
    event.preventDefault(); // Prevenir comportamiento predeterminado del botón

    var form = document.getElementById("formDeleteCard");
    Swal.fire({
        title: 'Estas seguro?',
        text: "No podrás deshacer la acción!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si, borralo!',
        cancelButtonText: "Cancelar"
      }).then((result) => {
        if (result.isConfirmed) {
          Swal.fire(
            'Eliminado!',
            'Tarjeta eliminada correctamente.',
            'success'
          ).then(function () {
            form.submit(); // Enviar el formulario manualmente
        });
        }
      })
}

