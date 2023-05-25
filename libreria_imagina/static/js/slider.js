$(document).ready(function () {
    $("#libro-slider").owlCarousel({
        nav: true,
        navText: ["<div class='nav-button owl-prev d-none d-md-none d-lg-block'><i class='fa-solid fa-chevron-left'></i></div>", "<div class='nav-button owl-next d-none d-md-none d-lg-block'><i class='fa-solid fa-chevron-right'></i></div>"],
        stagePadding: 0,
        loop: true,
        dots: false,
        margin: 5,
        responsiveClass: true,
        items: 5,
        autoplay: true,
        autoplayTimeout: 3000,
        autoplayHoverPause: true,
        responsive: {
            0: {
                items: 1,
            },
            580: {
                items: 2, // Cambiar de 3 a 2
            },
            780: {
                items: 3, // Cambiar de 3 a 2
            },
            1000: {
                items: 4, // Cambiar de 3 a 2
            },
            1200: {
                items: 5,
            }
        }
    });
});
