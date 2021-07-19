function previewFile() {
    var preview = document.querySelector('.avatarPreview');
    var file    = document.querySelector('input[type=file]').files[0];
    var reader  = new FileReader();
  
    reader.onloadend = function () {
      preview.src = reader.result;
    }
  
    if (file) {
      reader.readAsDataURL(file);
    } else {
      preview.src = "";
    }
  }

function getFormData(needle) {
    return document.querySelector("#" + needle).value;
}

function sendRequest(id) {
    let query = '?id='+ id;

    query += "&name=" + getFormData("name");
    query += "&surname=" + getFormData("surname");
    if (getFormData("password")) {
        query += "&password=" + getFormData("password");
    }
    query += "&email=" + getFormData("email");
    if (getFormData("phone")) {
        query += "&phone=" + getFormData("phone");
    }
    if (getFormData("viber") != "None") {
        query += "&viber=" + getFormData("viber");
    }
    if (getFormData('userType') != "noChange" && getFormData("userType") != getFormData("prevType")) {
        query += "&userType=" + getFormData("userType");
        query += "&prevType=" + getFormData("prevType");
    }
    relocateUser(query);
}