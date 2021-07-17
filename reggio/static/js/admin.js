function invertCheckState() {
    let checkboxes = document.querySelectorAll('.rowSelect')

    checkboxes.forEach(checkbox => {
        checkbox.checked = this.checked ? true : false
    })
}

function decheckCheckState() {
    let checkboxes = document.querySelectorAll('.rowSelect')
    let checkAll = document.querySelector('#checkAll');

    checkAll.checked = false
    checkboxes.forEach(checkbox => {
        checkbox.checked = false
    })
}


function deleteIndividuals() {
    let checkboxes = document.querySelectorAll('.rowSelect')


    let toDel = []
    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            toDel.push(checkbox.getAttribute('classid').toString())
        }
    })
    console.log(toDel)
    axios.get('/admin/deleteIndividualClasses?ids='+toDel.join(';'))
    .then(response => {
        window.location = response.data == "0" ? "/admin/individualClasses" : "/admin/individualClasses?error=1"
    })
}

function downloadIndividuals() {
    let preferredFilename = document.querySelector('#preferredFilename').value
    let toDownload = []

    document.querySelectorAll('.rowSelect').forEach(checkbox => {
        if (checkbox.checked) {
            toDownload.push(checkbox.getAttribute('classid').toString())
        }
    })

    console.log(toDownload)
    axios.get('/admin/createIndividualClassXLSX?ids='+toDownload.join(';')+"&prefferedFilename="+preferredFilename)
    .then(response => {
        if (response.data == "1") {
            window.location = "/admin/individualClasses?error=1"
        }
        else {
            window.open('/admin/downloadXLSX?filename='+response.data)
            window.location = "/admin/individualClasses"
        }
    })
}

document.addEventListener('DOMContentLoaded', () => {
    let checkAll = document.querySelector('#checkAll');

    checkAll.addEventListener('click', invertCheckState)
})