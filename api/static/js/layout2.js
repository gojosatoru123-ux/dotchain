document.addEventListener('DOMContentLoaded', function() {
  var angles = document.querySelectorAll('.angle');
  for (var i = 0; i < angles.length; i++) {
    angles[i].addEventListener('click', function(e) {
      this.classList.toggle('arrow');
    });
  }
  angles[0].classList.add('first');
  angles[angles.length - 1].classList.add('last');
});