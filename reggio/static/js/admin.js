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
        alert('Ви не обрали жодну індивідуалку');
        return
    }

    axios.get('/admin/deleteIndividualClasses?ids='+toDel.join(';'))
    .then(response => {
        document.location.reload();
    })
}

function downloadMany() {
    let checkboxes = document.querySelectorAll('.rowSelect')
    let preferredFilename = document.querySelector('#preferredFilename').value

    let toDownload = []
    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            toDownload.push(checkbox.getAttribute('classid').toString())
        }
    })
    if (toDownload.length <= 0) {
        alert('Ви не обрали жодну індивідуалку');
        return
    }

    axios.get('/admin/createIndividualClassXLSX?ids='+toDownload.join(';'))
    .then(response => {
        console.log(response.data)
        window.open('/admin/downloadXLSX?preferredFilename='+preferredFilename+'&filename='+response.data)
        axios.get('/admin/deleteXLSX?filename='+response.data)
    })
}

document.addEventListener('DOMContentLoaded', () => {
    let checkAll = document.querySelector('#checkAll');

    checkAll.addEventListener('click', changeCheckState)
})