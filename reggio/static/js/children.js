function bindParent(element) {
    let children = element.parentNode.childNodes;
    let userID = element.parentNode.id;
    element.innerText = 'bind';
    let txt = element.innerHTML
    console.log(txt)
    children.forEach(element => {
        if (element.nodeType == 1) {
            if (element.classList.contains('parents')) {
                element.innerHTML +='<input autocomplete="off" id="newParent" list="parentList" type="text">';
            }
        }
    });
    element.onclick = sendRequest;
}

function sendRequest() {
    let query = '?id='+String(this.parentNode.id);
    let parent = this.parentNode.querySelector('.parents')
    let inputField = parent.querySelector("#newParent")
    let newParent = inputField.value
    inputField.parentNode.removeChild(inputField)
    if(parent.innerHTML !== "None" || parent.innerHTML !== '')
        query += '&parents='+parent.innerHTML + ';' + newParent;
    else
        query += '&parents='+ newParent;
    relocateUser(query);
}