window.addEventListener('scroll', function() {
      var heroSection = document.querySelector('.articleheader');
      var scrollPosition = window.pageYOffset;

      heroSection.style.backgroundSize = (100 + scrollPosition / 5) + '%';
    });