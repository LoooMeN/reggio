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

function triggerMenu() {
    let menu = document.querySelector('.menuBox');

    if (!menu.classList.contains('collapsedMenu')) {
        menu.classList.add('collapsedMenu')
        setTimeout(() => {
            menu.style.display = "none";
        }, 250);
    }
    else {
        menu.style.display = "flex";
        setTimeout(() => {
            menu.classList.remove('collapsedMenu')
        }, 50);
    }
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
    let menu = document.querySelector('.menuBox');

    if (window.screen.width <= 1500) {
        menu.classList.add('collapsedMenu')
    }
}

function triggerProfile() {
    let profileBox = document.querySelector('#profileBox');

    console.log("flex")
    profileBox.classList.contains('collapsedMenu') ? profileBox.classList.remove('collapsedMenu') : profileBox.classList.add('collapsedMenu')
}

function optimizeTableHeight() {
    let tableWrapper = document.querySelector('.tableWrapper');

    if (tableWrapper) {
        let offset = document.querySelector('.titleWrapper').scrollHeight + 50;
        let bonusOffset = document.querySelector('#bonusOffset');
        
        if (bonusOffset) {
            offset += document.querySelector(bonusOffset.getAttribute('value')).scrollHeight;
        }

        if (tableWrapper)
            tableWrapper.style.height = window.innerHeight - offset - 20 + "px";
    }
}

function tableCellExpandTrigger() {
    let tableWrapper = document.querySelector('.tableWrapper');

    if (tableWrapper) {
        let cells = tableWrapper.querySelectorAll('.name');

        cells.forEach((cell) => {
            cell.addEventListener('click', () => {
                cell.parentNode.classList.contains('cellExpanded') ? cell.parentNode.classList.remove('cellExpanded') : cell.parentNode.classList.add('cellExpanded')
            });
        });
    }
}

function fixMobileHeight() {
    let vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
}

document.addEventListener('DOMContentLoaded', () => {
    handleCollapsedMenuItems();
    handleErrors();
    handleCollapseTablet();
    optimizeTableHeight();
    tableCellExpandTrigger();
    fixMobileHeight();
    window.addEventListener('resize', fixMobileHeight)
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
    relocateProfile(query);
}