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
            searchElement.style.display = searchElement.getAttribute('prevState');
        } else {
            if (searchElement.getAttribute('prevState') && searchElement.style.display != "none")
                searchElement.setAttribute('prevState', searchElement.style.display)
            searchElement.style.display = "none";
        }
    });
}

function modalHandler() {
    let openModalTrigger = document.querySelector('#modalTrigger');
    let modalBg = document.querySelector('#modalBackground');
    let modal = document.querySelector('#sideItemModal');
    let closeModalTrigger = document.querySelector('#closeModal');

    if (!modal) {
        openModalTrigger.style.display = 'none';
    } else {
        openModalTrigger.addEventListener('click', () => {
            modalBg.style.display = 'block';
            modal.style.display = 'block';
        });
        closeModalTrigger.addEventListener('click', () => {
            modalBg.style.display = 'none';
            modal.style.display = 'none';
        })
    }
}