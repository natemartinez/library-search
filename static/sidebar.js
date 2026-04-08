document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('sidebar');
    const toggle = document.getElementById('sidebar-toggle');
    const sidebarLinks = document.querySelectorAll('#sidebar a');

    if (!sidebar || !toggle) return;

    // Restore persisted state before first paint
    if (localStorage.getItem('sidebar-collapsed') === 'true') {
        sidebar.classList.add('collapsed');
    }

    toggle.addEventListener('click', function () {
        sidebar.classList.toggle('collapsed');
        localStorage.setItem('sidebar-collapsed', sidebar.classList.contains('collapsed'));
    });
    
    sidebarLinks.forEach(link => {
        const linkPath = new URL(link.href).pathname;
        if (linkPath === window.location.pathname) {
            link.children[0].classList.add('on');
        }
    });
});
