document.addEventListener('DOMContentLoaded', function() {
  var modal = document.querySelector('.modal');
  var closeModalButton = document.querySelector('#closeModalButton');
  var submitButton = document.querySelector('#submitButton');
  var form = document.querySelector('#myForm');
  var formularioEnviadoValue = document.getElementById('formularioEnviadoValue').getAttribute('data-formulario-enviado');
  var formularioEnviado = JSON.parse(formularioEnviadoValue);

  if (formularioEnviado) {
    modal.style.display = 'block';
  }

  submitButton.addEventListener('click', function(e) {
    e.preventDefault();

    var formFields = form.querySelectorAll('input, textarea, select');
    var formValid = true;

    // Validar cada campo del formulario
    formFields.forEach(function(field) {
      if (!field.checkValidity()) {
        field.reportValidity();
        formValid = false;
      }
    });

    if (formValid) {
      fetch(form.action, {
        method: form.method,
        body: new FormData(form)
      })
      .then(function(response) {
        modal.style.display = 'block';
        form.reset();
      })
      .catch(function(error) {
        console.error('Error:', error);
      });
    }
  });

  closeModalButton.addEventListener('click', function() {
    modal.style.display = 'none';
  });

  window.addEventListener('click', function(event) {
    if (event.target === modal) {
      modal.style.display = 'none';
    }
  });
});
