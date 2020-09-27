function changeCheckState() {
    let checkboxes = document.querySelectorAll('.rowSelect')

    checkboxes.forEach(checkbox => {
        checkbox.checked = this.checked ? true : false
    })
}

function deleteMany() {
    let checkboxes = document.querySelectorAll('.rowSelect')

    let toDel = []
    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            toDel.push(checkbox.getAttribute('classid').toString())
        }
    })
    if (toDel.length <= 0) {
        alert('Ви не обрали не одну індивідуалку');
        return
    }
    axios.get('/admin/deleteIndividualClasses?api=1&ids='+toDel.join(';'))
    .then(response => {
        document.location.reload();
    })
}

document.addEventListener('DOMContentLoaded', () => {
    let checkAll = document.querySelector('#checkAll');

    checkAll.addEventListener('click', changeCheckState)
})