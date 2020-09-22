function editUser(element) {
    let children = element.parentNode.childNodes;
    let userID = element.parentNode.id;
    element.innerText = 'save';
    children.forEach(element => {
        if (element.nodeType == 1) {
            if (element.classList.contains('text')) {
                element.setAttribute('contenteditable', 'true');
            }
            if (element.classList.contains('link')) {
                element.innerText = element.childNodes[0].href;
            }
            if (element.classList.contains('image')) {
                // #todo
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
    let children = this.parentNode.childNodes;
    let query = '?id='+String(this.parentNode.id);
    children.forEach(element => {
        if (element.nodeType == 1) {
            if (element.classList.contains('phone')) {
                query += '&phone='+element.innerText;
            }
            if (element.classList.contains('name')) {
                query += '&name='+element.innerText;
            }
            if (element.classList.contains('email')) {
                query += '&email='+element.innerText;
            }
            if (element.classList.contains('surname')) {
                query += '&surname='+element.innerText;
            }
            if (element.classList.contains('select')) {
                query += '&userType='+element.childNodes[0].value;
                query += '&prevType='+element.getAttribute('prev');
            }
            if (element.classList.contains('viber')) {
                query += '&viber='+element.innerText;
            }
        }
    });
    relocateUser(query);
}