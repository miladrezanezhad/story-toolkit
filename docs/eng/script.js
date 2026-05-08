/* ============================================
   Story Development Toolkit - Scripts
   Author: Milad Rezanezhad
   ============================================ */

// ============================================================
// Copy Code Functionality
// ============================================================

function copyCode(button) {
    const wrapper = button.closest('.code-block-wrapper');
    if (!wrapper) return;
    
    const codeBlock = wrapper.querySelector('code');
    if (!codeBlock) return;
    
    const text = codeBlock.innerText;
    
    navigator.clipboard.writeText(text).then(() => {
        const originalHTML = button.innerHTML;
        button.innerHTML = '<i class="fa-solid fa-check"></i> Copied!';
        showToast('✅ Code copied!');
        setTimeout(() => {
            button.innerHTML = originalHTML;
        }, 2000);
    }).catch(() => {
        showToast('❌ Copy failed', 'error');
    });
}

// ============================================================
// Toast Notification
// ============================================================

function showToast(message, type = 'success') {
    const existing = document.querySelector('.toast-copy');
    if (existing) existing.remove();
    
    const toast = document.createElement('div');
    toast.className = `toast-copy ${type}`;
    toast.innerHTML = `<span>${message}</span>`;
    document.body.appendChild(toast);
    
    setTimeout(() => toast.classList.add('show'), 10);
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ============================================================
// Active Navbar Link (Top Navigation)
// ============================================================

function setActiveNavLink() {
    // Get current filename from URL
    let currentPage = window.location.pathname.split('/').pop();
    if (!currentPage || currentPage === '') {
        currentPage = 'index.html';
    }
    
    console.log('Current page:', currentPage);
    
    document.querySelectorAll('.nav-link').forEach(link => {
        const href = link.getAttribute('href');
        // Remove any existing active class
        link.classList.remove('active');
        
        // Check if this link matches current page
        if (href === currentPage) {
            link.classList.add('active');
            console.log('Active link found:', href);
        }
        
        // Special case for index.html
        if (currentPage === 'index.html' && (href === 'index.html' || href === '.' || href === './')) {
            link.classList.add('active');
        }
    });
}

// ============================================================
// Scroll Spy for Sidebar
// ============================================================

function initScrollSpy() {
    const sidebarLinks = document.querySelectorAll('.nav-link-sidebar');
    if (sidebarLinks.length === 0) {
        console.log('No sidebar links found');
        return;
    }
    
    // Get all sections
    const sections = [];
    sidebarLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && href.startsWith('#')) {
            const section = document.querySelector(href);
            if (section) {
                sections.push({
                    link: link,
                    section: section,
                    id: href.substring(1)
                });
                console.log('Section found:', href);
            } else {
                console.log('Section not found:', href);
            }
        }
    });
    
    if (sections.length === 0) return;
    
    function updateActiveLink() {
        const scrollPosition = window.scrollY + 150; // Offset for fixed header
        
        let currentSection = null;
        
        // Find which section is currently in view
        for (const item of sections) {
            const sectionTop = item.section.offsetTop;
            const sectionBottom = sectionTop + item.section.offsetHeight;
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
                currentSection = item;
                break;
            }
        }
        
        // If scrolled to top, highlight first section
        if (!currentSection && window.scrollY < 100 && sections.length > 0) {
            currentSection = sections[0];
        }
        
        // If scrolled to bottom, highlight last section
        if (!currentSection && (window.innerHeight + window.scrollY) >= document.body.offsetHeight - 100) {
            currentSection = sections[sections.length - 1];
        }
        
        // Update active class on links
        sections.forEach(item => {
            if (currentSection && item.id === currentSection.id) {
                item.link.classList.add('active');
            } else {
                item.link.classList.remove('active');
            }
        });
    }
    
    // Initial call
    updateActiveLink();
    
    // Add scroll listener with debounce for performance
    let ticking = false;
    window.addEventListener('scroll', () => {
        if (!ticking) {
            requestAnimationFrame(() => {
                updateActiveLink();
                ticking = false;
            });
            ticking = true;
        }
    });
    
    // Also update on resize
    window.addEventListener('resize', updateActiveLink);
    
    console.log('Scroll spy initialized with', sections.length, 'sections');
}

// ============================================================
// Smooth Scroll for Anchor Links
// ============================================================

function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#' || targetId === '') return;
            
            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'start' 
                });
                // Update URL without reload
                history.pushState(null, null, targetId);
                
                // Also update active state manually after click
                setTimeout(() => {
                    const event = new Event('scroll');
                    window.dispatchEvent(event);
                }, 100);
            }
        });
    });
}

// ============================================================
// Fix Sidebar Position
// ============================================================

function fixSidebarPosition() {
    const sidebar = document.querySelector('.sidebar-custom');
    if (!sidebar) return;
    
    const navbar = document.querySelector('.navbar');
    const headerHeight = navbar ? navbar.offsetHeight : 70;
    sidebar.style.top = `${headerHeight + 10}px`;
}

// ============================================================
// Add Toast Styles
// ============================================================

function addToastStyles() {
    if (document.getElementById('toast-styles')) return;
    
    const style = document.createElement('style');
    style.id = 'toast-styles';
    style.textContent = `
        .toast-copy {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #3fb950;
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 14px;
            z-index: 9999;
            opacity: 0;
            transform: translateY(20px);
            transition: all 0.3s ease;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        .toast-copy.show {
            opacity: 1;
            transform: translateY(0);
        }
        .toast-copy.error {
            background: #f85149;
        }
        .nav-link-sidebar.active {
            background: rgba(88, 166, 255, 0.15);
            color: #58a6ff !important;
            border-left: 2px solid #58a6ff;
        }
        .nav-link-sidebar.active i {
            color: #58a6ff;
        }
    `;
    document.head.appendChild(style);
}

// ============================================================
// Initialize Everything
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('Story Toolkit - Documentation loading...');
    
    setActiveNavLink();
    fixSidebarPosition();
    initSmoothScroll();
    addToastStyles();
    initScrollSpy(); // Initialize after sections are loaded
    
    console.log('✅ All scripts initialized');
});

// Re-run scroll spy after all images/fonts load
window.addEventListener('load', () => {
    // Force scroll spy update
    window.dispatchEvent(new Event('scroll'));
    console.log('🔄 Scroll spy updated after load');
});

// Handle dynamic content changes (for any future updates)
const observer = new MutationObserver(() => {
    window.dispatchEvent(new Event('scroll'));
});
observer.observe(document.body, { childList: true, subtree: true });
