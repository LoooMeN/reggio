// applies search inside table fields
function searchInput() {
    let input = document.querySelector('#searchInput').value.toUpperCase();
    let searchContainer = document.querySelector('table[search=true]');;
    let searchElements = searchContainer.querySelectorAll('tr[searchable=true]');

    searchElements.forEach(searchElement => {
        let searchFields = searchElement.querySelectorAll('td[searchable=true]')
        let searchString = "";
        searchFields.forEach(element => {
            searchString += element.innerText;
        })
        searchString = searchString.toUpperCase();
        if (searchString.includes(input)) {
            searchElement.style.display = "";
        } else {
            searchElement.style.display = "none";
        }
    });
}

