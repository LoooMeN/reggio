// applies search inside table fields
function searchInput() {
    let input = document.querySelector('#searchInput').value.toUpperCase();
    let searchContainer = document.querySelector('div[search=true]');;
    let searchElements = searchContainer.querySelectorAll('.Row[searchable=true]');

    searchElements.forEach(searchElement => {
        let searchFields = searchElement.querySelectorAll('div[searchable=true]')
        let searchString = "";
        searchFields.forEach(element => {
            searchString += element.innerText;
        })
        searchString = searchString.toUpperCase();
        if (searchString.includes(input)) {
            console.log(searchElement)
            searchElement.style.display = "contents";
        } else {
            console.log(searchElement)
            searchElement.style.display = "none";
        }
    });
}