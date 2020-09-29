function handleCollapsedMenuItems() {
    let menuItemsWithSubmenu = document.querySelectorAll('.hasSubMenu');
    
    menuItemsWithSubmenu.forEach(menuItem => {
        menuItem.addEventListener('click', () => {
            let subMenu = menuItem.querySelector('.subMenu')
            if (subMenu.classList.contains('collapsed')) {
                console.log('test')
                subMenu.classList.remove('collapsed')
            } else {
                subMenu.classList.add('collapsed')
            }
        })
    })
}

document.addEventListener('DOMContentLoaded', () => {
    handleCollapsedMenuItems();
})