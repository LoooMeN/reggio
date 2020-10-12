function handleCollapsedMenuItems() {
    let menuItemsWithSubmenu = document.querySelectorAll('.menuItem');
    
    menuItemsWithSubmenu.forEach(menuItem => {
        menuItem.addEventListener('click', (event) => {
            parent = menuItem.parentElement;
            let elements = parent.querySelector('.subMenu')
            let selectedMenuItem = parent.querySelector('.menuItem')
            if (elements) {
                if (elements.classList.contains('collapsed')) {
                    elements.classList.remove('collapsed')
                    selectedMenuItem.classList.add('menuItemHovered')
                } else {
                    elements.classList.add('collapsed')
                    selectedMenuItem.classList.remove('menuItemHovered')
                }
            }
        })
    })
}

function handleCollapseMenu() {
    let trigger = document.querySelector('#collapseTrigger');
    let menu = document.querySelector('.menuBox');

    trigger.addEventListener('click', () => {
        if (menu.classList.contains('collapsedMenu')) {
            trigger.classList.remove('triggered')
            menu.classList.remove('collapsedMenu')
            trigger.style.top = '31px'
        } else {
            trigger.classList.add('triggered')
            menu.classList.add('collapsedMenu')
            trigger.style.top = '0px'
        }
    })
}

function handleErrors() {
    let errorsBox = document.querySelector('#errorsBox');
    let closeErrors = document.querySelector('#closeErrors')

    if (errorsBox.querySelector('.error')) {
        errorsBox.style.display = 'flex';
        closeErrors.addEventListener('click', () => {
            errorsBox.style.right = '-380px';
            setTimeout(() => {
                errorsBox.remove();
            }, 800);
        })
    }
}

function handleCollapseTablet() {
    let trigger = document.querySelector('#collapseTrigger');
    let menu = document.querySelector('.menuBox');
    let openModalTrigger = document.querySelector('#tabletTrigger');
    let modalBg = document.querySelector('#modalBackground');
    let modal = document.querySelector('#sideItemModal');
    let closeModalTrigger = document.querySelector('#closeModal');

    if (window.screen.width <= 1500) {
        trigger.classList.add('triggered')
        menu.classList.add('collapsedMenu')
        if (!modal) {
            openModalTrigger.style.display = 'none';
        } else {
            openModalTrigger.addEventListener('click', () => {
                modalBg.style.display = 'block';
                modal.style.right = 'initial';
            });
            closeModalTrigger.addEventListener('click', () => {
                modalBg.style.display = 'none';
                modal.style.right = '-500px';
            })
        }
    }
}

function handleCollapseProfile() {
    let profileTrigger = document.querySelector('#triggerProfile');
    let profileBox = document.querySelector('#profileBox');
    let closeProfile = document.querySelector('#closeProfile');
    let trigger = document.querySelector('#collapseTrigger');
    let saveButton = document.querySelector('#saveButton');

    if (profileTrigger) {
        profileTrigger.addEventListener('click', () => {
            profileBox.classList.remove('collapsedMenu');
            trigger.style.top = '-100px';
        });
        closeProfile.addEventListener('click', () => {
            profileBox.classList.add('collapsedMenu');
            trigger.style.top = '31px';
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    handleCollapsedMenuItems();
    handleCollapseMenu();
    handleErrors();
    handleCollapseTablet();
    handleCollapseProfile();
})

function previewFileChangeAvatar() {
    let preview = document.querySelector('#currentUserAvatar');
    let file    = document.querySelector('#changeAvatar').files[0];
    let reader = new FileReader();

    reader.onloadend = function () {
      preview.src = reader.result;
    }
  
    if (file) {
      reader.readAsDataURL(file);
    } else {
      preview.src = "";
    }
}

function submitProfileChanges(){
    let query = '?id=' + document.querySelector('input[name="profileId"]').value ;
    let name = document.querySelector('input[name="profileName"]').value
    let surname = document.querySelector('input[name="profileSurname"]').value
    let email = document.querySelector('input[name="profileEmail"]').value
    let phone = document.querySelector('input[name="profilePhone"]').value
    let viber = document.querySelector('input[name="profileViber"]').value
    query += '&name=' + name +
             '&surname=' + surname +
             '&email=' + email +
             '&phone=' + phone +
             '&viber=' + viber;
    relocateUser(query);
}