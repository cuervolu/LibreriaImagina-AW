// Agrega un controlador de eventos para cada botón de incremento
var incrementButtons = document.querySelectorAll(".incrementButton");
incrementButtons.forEach(function (button) {
    button.addEventListener("click", function () {
        var input = button.closest(".input-group").querySelector(".count");
        input.value = parseInt(input.value) + 1;
    });
});

// Agrega un controlador de eventos para cada botón de decremento
var decrementButtons = document.querySelectorAll(".decrementButton");
decrementButtons.forEach(function (button) {
    button.addEventListener("click", function () {
        var input = button.closest(".input-group").querySelector(".count");
        if (input.value > 1) {
            input.value = parseInt(input.value) - 1;
        }
    });
});