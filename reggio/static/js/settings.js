
function saveStyleSettings(element) {
    let div = element.parentNode;
    let selectInput = document.querySelectorAll('#value');
    let query = '?id=save';
    query += '&values=';
    selectInput.forEach(element => {
        if(element.type === 'color'){
            query += element.name + " " + element.value.replace('#', '%23') + ";";
        }
        else
            query += element.name + " " + element.value + ";";
    })

    console.log(query);
    relocateUser(query);
}
