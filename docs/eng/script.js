/* ============================================
   Story Development Toolkit - Scripts
   Copy + Toast + Sidebar Scroll Spy
   Author: Milad Rezanezhad
   GitHub: https://github.com/miladrezanezhad
   ============================================ */

function copyCode(button) {
    const wrapper = button.closest('.code-block-wrapper');
    const codeBlock = wrapper.querySelector('code');
    const text = codeBlock.innerText;

    navigator.clipboard.writeText(text).then(() => {
        button.innerHTML = '<i class="fa-solid fa-check"></i> Copied';
        button.classList.add('copied');
        showToast('✅ Code copied successfully!');
        setTimeout(() => {
            button.innerHTML = '<i class="fa-regular fa-copy"></i> Copy';
            button.classList.remove('copied');
        }, 2000);
    }).catch(() => {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        button.innerHTML = '<i class="fa-solid fa-check"></i> Copied';
        button.classList.add('copied');
        showToast('✅ Code copied successfully!');
        setTimeout(() => {
            button.innerHTML = '<i class="fa-regular fa-copy"></i> Copy';
            button.classList.remove('copied');
        }, 2000);
    });
}

function showToast(message) {
    const existing = document.querySelector('.toast-copy');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'toast-copy';
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => toast.classList.add('show'), 100);
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Active nav link
document.addEventListener('DOMContentLoaded', () => {
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath.split('/').pop()) {
            link.classList.add('active');
        }
    });
});

// Sidebar scroll spy
document.addEventListener('DOMContentLoaded', () => {
    const sidebarLinks = document.querySelectorAll('.nav-link-sidebar');
    const sections = [];

    sidebarLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && href.startsWith('#')) {
            const section = document.querySelector(href);
            if (section) {
                sections.push({ link, section, id: href.slice(1) });
            }
        }
    });

    function onScroll() {
        let currentId = '';
        const scrollY = window.scrollY + 100;

        sections.forEach(({ section, id }) => {
            if (scrollY >= section.offsetTop) {
                currentId = id;
            }
        });

        sidebarLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${currentId}`) {
                link.classList.add('active');
            }
        });
    }

    window.addEventListener('scroll', onScroll);
    onScroll();
});
