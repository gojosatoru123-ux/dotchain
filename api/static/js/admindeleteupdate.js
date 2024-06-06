function openForm(event) {
  var formId = event.target.getAttribute('data-form-id');
  document.getElementById(formId).style.display = "block";
}

function closeForm(event) {
  var formId = event.target.getAttribute('data-form-id');
  document.getElementById(formId).style.display = "none";
}
