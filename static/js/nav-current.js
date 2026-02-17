// Highlight the current nav link based on URL path
(function() {
  var path = window.location.pathname;
  // Normalize: remove trailing slash
  if (path.length > 1 && path.endsWith('/')) {
    path = path.slice(0, -1);
  }
  var navLinks = document.querySelectorAll('.nav-menu .nav-link');
  navLinks.forEach(function(link) {
    var href = link.getAttribute('href');
    if (!href) return;
    // Remove trailing slash from href too
    if (href.length > 1 && href.endsWith('/')) {
      href = href.slice(0, -1);
    }
    // Match: exact path or home page
    if (href === path || (href === '/' && path === '') || (href === '' && path === '/')) {
      link.classList.add('w--current');
    } else {
      link.classList.remove('w--current');
    }
  });
})();
