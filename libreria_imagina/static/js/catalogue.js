document.addEventListener('DOMContentLoaded', function () {
    var cantidadInputs = document.querySelectorAll(".cantidad");
    cantidadInputs.forEach(function (cantidadInput) {
        cantidadInput.value = 1;
    });

    var aumentarCantidadLinks = document.querySelectorAll(".aumentar-cantidad");
    var agregarCarritoIcons = document.querySelectorAll(".agregar-carrito-icon");

    aumentarCantidadLinks.forEach(function (link) {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            var cantidadInput = link.parentNode.parentNode.parentNode.querySelector(".cantidad");
            var cantidadDisponible = parseInt(cantidadInput.getAttribute("data-disponible"));
            var cantidadActual = parseInt(cantidadInput.value);
            if (cantidadActual < cantidadDisponible) {
                cantidadInput.value = cantidadActual + 1;
            }
        });
    });

    agregarCarritoIcons.forEach(function (icon) {
        icon.addEventListener('click', function (event) {
            event.preventDefault();
            var form = icon.parentNode.parentNode.parentNode.parentNode;
            var cantidadInput = form.querySelector(".cantidad");
            cantidadInput.value = parseInt(cantidadInput.value);
            form.submit();
        });
    });
});
