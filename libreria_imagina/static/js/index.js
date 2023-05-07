function footerText() {
    console.log('footerText() called');
    const footerText = document.getElementById('footer-text');
    if (footerText) {
      const currentYear = new Date().getFullYear();
      footerText.innerHTML = `Todos los derechos reservados © 2003-${currentYear} LIBRERÍA IMAGINA`;
    }
  }
  
  footerText();
