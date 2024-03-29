function bindParent(element) {
    let parentNode = element.parentNode.parentNode;
    let userID = parentNode.id;
    parentNode.querySelector('.relatives').innerHTML += '<input autocomplete="off" id="newParent" list="parentList" type="text">';
    let parentNames = parentNode.querySelectorAll('.parent')
    
    parentNames.forEach(element => {
        element.innerHTML += "<img src='static/images/icons/cross.svg' onclick='removeParent(this)'>"
    })
    element.onclick = sendRequest;
}

function sendRequest() {
    let query = '?id='+String(this.parentNode.parentNode.id);

    let parents = this.parentNode.parentNode.querySelector('.relatives');
    let newParent = parents.querySelector("#newParent").value;
    let children = parents.querySelectorAll('p');

    prevParents = '';
    children.forEach(element => {
        prevParents += element.innerHTML + ';';
    });
    query += '&parents='+ prevParents + newParent;
    relocateUser(query);
}