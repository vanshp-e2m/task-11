(function() {
    var b = document.querySelector('.site-head__toggle');
    if (!b) return;
    b.addEventListener('click', function() {
        var o = b.getAttribute('aria-expanded') === 'true';
        b.setAttribute('aria-expanded', String(!o));
        document.getElementById('site-primary-nav').classList.toggle('is-open', !o);
        document.body.classList.toggle('nav-open', !o);
    });
})();