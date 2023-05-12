$(document).ready(function () {
    $("#libro-slider").owlCarousel({
        nav: true,
        navText: ["<div class='nav-button owl-prev'><i class='fa-solid fa-chevron-left'></i></div>", "<div class='nav-button owl-next'><i class='fa-solid fa-chevron-right'></i></div>"],
        stagePadding: 0,
        loop: true,
        dots: false,
        margin: 5,
        responsiveClass: true,
        items: 5,
        autoplay: true,
        autoplayTimeout: 1000,
        autoplayHoverPause: true,
        responsive: {
            0: {
                items: 1,
            },
            600: {
                items: 2, // Cambiar de 3 a 2
            },
            1000: {
                items: 5,
            }
        }
    });
});
