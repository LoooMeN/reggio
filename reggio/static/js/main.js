function handleCollapsedMenuItems() {
    let menuItemsWithSubmenu = document.querySelectorAll('.dropdownArrow');
    
    menuItemsWithSubmenu.forEach(menuItem => {
        menuItem.addEventListener('click', (event) => {
            parent = menuItem.parentElement.parentElement.parentElement
            let elements = parent.querySelector('.subMenu')
            let selectedMenuItem = parent.querySelector('.menuItem')
            if (elements.classList.contains('collapsed')) {
                elements.classList.remove('collapsed')
                selectedMenuItem.classList.add('menuItemHovered')
            } else {
                elements.classList.add('collapsed')
                selectedMenuItem.classList.remove('menuItemHovered')
            }
        })
    })
}

document.addEventListener('DOMContentLoaded', () => {
    handleCollapsedMenuItems();
})