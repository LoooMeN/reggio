function bindParent(element) {
    let children = element.parentNode.childNodes;
    let userID = element.parentNode.id;
    let input = document.createElement("input");
    input.setAttribute("list","parentList");
    input.setAttribute("type","text");
    input.setAttribute("autocomplete","off");
    element.innerText = 'save';
    children.forEach(element => {
        if (element.nodeType == 1) {
            if (element.classList.contains('parents')) {
                    element.innerHTML +='<br>' + '<input autocomplete="off" list="parentList" type="text">';
            }
        }
    });
    element.onclick = sendRequest;
}

function sendRequest() {
    let query = '?id='+String(this.parentNode.id);
    let parent = this.parentNode.querySelector('.parents')
    query += '&parents='+parent.innerHTML - ();
    relocateUser(query);
}