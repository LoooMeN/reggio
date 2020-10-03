function bindParent(element) {
    let parentNode = element.parentNode;
    let userID = parentNode.id;
    element.innerText = 'bind';
    parentNode.querySelector('.parents').innerHTML += '<input autocomplete="off" id="newParent" list="parentList" type="text">';
    element.onclick = sendRequest;
}

function sendRequest() {
    let query = '?id='+String(this.parentNode.id);

    let parents = this.parentNode.querySelector('.parents');
    let newParent = parents.querySelector("#newParent").value;
    let children = parents.querySelectorAll('.parent');

    prevParents = '';
    children.forEach(element => {
        prevParents += element.innerHTML + ';'
    });
    query += '&parents='+ prevParents + newParent;
    relocateUser(query);
}