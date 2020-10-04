
function getValue(element) {
    let div = element.parentNode;
    let selectInput = document.querySelectorAll('#value');
    let query = '?id=save';
    query += '&values=';
    selectInput.forEach(element => {
        if(element.name === 'color'){
            query += '\\' + element.value + ";";
        }
        else query += element.value + ";";
    })

    console.log(query)
    relocateUser(query);

}
