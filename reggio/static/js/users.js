function previewFile() {
    var preview = document.querySelector('.avatarPreview');
    var file    = document.querySelector('input[type=file]').files[0];
    var reader  = new FileReader();
  
    console.log('sex')
    reader.onloadend = function () {
      preview.src = reader.result;
    }
  
    if (file) {
      reader.readAsDataURL(file);
    } else {
      preview.src = "";
    }
  }

function editUser(element) {
    let children = element.parentNode.parentNode.childNodes;
    let userID = element.parentNode.parentNode.id;
    element.src= '/static/images/icons/confirm.svg';
    children.forEach(element => {
        if (element.nodeType == 1) {
            if (element.classList.contains('text')) {
                element.setAttribute('contenteditable', 'true');
            }
            if (element.classList.contains('link')) {
                if (element.childNodes[0]) {
                    element.innerText = 'None';
                } else {
                    element.innerText = element.childNodes[0].href;
                }
            }
            if (element.classList.contains('password')) {
                element.innerHTML = '<input type="password" id="password">';
            }
            if (element.classList.contains('select')) {
                let currentOption = element.innerText;
                let selectOptions = document.querySelector('#userType').outerHTML;
                element.setAttribute('prev', currentOption);
                element.innerHTML = selectOptions;
                element.querySelector('option[value="'+currentOption+'"]').selected='selected';
            }
        }
    });
    element.onclick = sendRequest;
}

function sendRequest() {
    console.log(this)
    let children = this.parentNode.parentNode.childNodes;
    let query = '?id='+String(this.parentNode.parentNode.id);
    children.forEach(element => {
        if (element.nodeType == 1) {
            if (element.classList.contains('phone')) {
                query += '&phone='+element.innerText;
            }
            if (element.classList.contains('password')) {
                query += '&password=' + document.getElementById('password').value
            }
            if (element.classList.contains('name')) {
                let text = element.innerText.split(' ')
                query += '&name='+text[0];
                query += '&surname='+text[1];
            }
            if (element.classList.contains('email')) {
                query += '&email='+element.innerText;
            }
            if (element.classList.contains('select')) {
                query += '&userType='+element.childNodes[0].value;
                query += '&prevType='+element.getAttribute('prev');
            }
            if (element.classList.contains('viber')) {
                if (element.innerText == 'None') {
                    query += '&viber=None';
                } else {
                    query += '&viber='+element.innerText;
                }
            }
        }
    });
    relocateUser(query);
}