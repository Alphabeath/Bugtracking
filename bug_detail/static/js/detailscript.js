document.addEventListener('DOMContentLoaded', function() {
  var modal = document.getElementById('myModal');
  var modalImg = document.getElementById('img01');
  var captionText = document.getElementById('caption');
  var close = document.getElementById('closeModal');
  var images = document.querySelectorAll('.card-img-top');

  images.forEach(function(image) {
    image.addEventListener('click', function() {
      modal.style.display = 'block';
      modalImg.src = this.src;
      captionText.innerHTML = this.alt;
    });
  });

  window.addEventListener('click', function(event) {
    if (event.target === modal) {
      modal.style.display = 'none';
    }
  });

  close.addEventListener('click', function() {
    modal.style.display = 'none';
  });
});
