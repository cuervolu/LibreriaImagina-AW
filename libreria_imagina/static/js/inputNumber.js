// Agrega un controlador de eventos para cada botón de incremento
var incrementButtons = document.querySelectorAll(".incrementButton");
incrementButtons.forEach(function (button) {
    button.addEventListener("click", function () {
        var input = button.closest(".input-group").querySelector(".count");
        input.value = parseInt(input.value) + 1;
        validateInput(input);
    });
});

// Agrega un controlador de eventos para cada botón de decremento
var decrementButtons = document.querySelectorAll(".decrementButton");
decrementButtons.forEach(function (button) {
    button.addEventListener("click", function () {
        var input = button.closest(".input-group").querySelector(".count");
        if (input.value > 1) {
            input.value = parseInt(input.value) - 1;
            validateInput(input);
        }
    });
});

// Función para validar el valor del campo de entrada
function validateInput(input) {
    var min = parseInt(input.getAttribute("min"));
    var max = parseInt(input.getAttribute("max"));
    var value = parseInt(input.value);

    if (isNaN(value) || value < min) {
        input.value = min;
    } else if (value > max) {
        input.value = max;
    }
}

