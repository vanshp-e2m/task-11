document.addEventListener('DOMContentLoaded', function() {
    var el = document.querySelector('#hero-carousel .hero-carousel__swiper');
    if (!el || !window.Swiper) return;
    new Swiper(el, {
        slidesPerView: 2,
        spaceBetween: 80,
        watchOverflow: true,
        pagination: {
            el: '#hero-carousel .hero-carousel__pagination',
            clickable: true
        },
        breakpoints: {
            0: {
                slidesPerView: 1,
                spaceBetween: 18
            },
            1024: {
                slidesPerView: 2,
                spaceBetween: 80
            }
        }
    });
});