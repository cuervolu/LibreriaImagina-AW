function footerText() {
    const footerText = document.getElementById('footer-text');
    if (footerText) {
      const currentYear = new Date().getFullYear();
      footerText.innerHTML = `Todos los derechos reservados © 2003-${currentYear} LIBRERÍA IMAGINA`;
    }
  }
  
  footerText();

  $(window).on('load', function(event) {
    $('.preloader').delay(500).fadeOut(500);
});