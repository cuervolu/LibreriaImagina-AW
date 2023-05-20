function increaseValue() {
    var input = document.querySelector('input[name="cantidad"]');
    var currentValue = parseInt(input.value);
    var maxValue = parseInt(input.getAttribute('max'));

    if (currentValue < maxValue) {
        input.value = currentValue + 1;
    }
}

function decreaseValue() {
    var input = document.querySelector('input[name="cantidad"]');
    var currentValue = parseInt(input.value);
    var minValue = parseInt(input.getAttribute('min'));

    if (currentValue > minValue) {
        input.value = currentValue - 1;
    }
}