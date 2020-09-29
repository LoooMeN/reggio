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
    let showMenu = document.querySelector('#showMenu');
    let menu = document.querySelector('.menuBox');

    trigger.addEventListener('click', () => {
        menu.classList.add('collapsedMenu')
    })

    showMenu.addEventListener('click', () => {
        menu.classList.remove('collapsedMenu')
    })
}

document.addEventListener('DOMContentLoaded', () => {
    handleCollapsedMenuItems();
    handleCollapseMenu();
})