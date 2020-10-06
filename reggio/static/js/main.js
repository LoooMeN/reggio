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
        } else {
            trigger.classList.add('triggered')
            menu.classList.add('collapsedMenu')
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

document.addEventListener('DOMContentLoaded', () => {
    handleCollapsedMenuItems();
    handleCollapseMenu();
    handleErrors();
})