var swiper = new Swiper(".slide-content", {
    watchSlidesProgress: true,
    spaceBetween: 25,
    loop: true,
    centeredSlides: false,
    loopFillGroupWithBlank: true,
    fade: true,
    grabCursor: true,
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
        dynamicBullets: true,
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    breakpoints: {
        520: {
            slidesPerView: 1,
        },
        700: {
            slidesPerView: 2,
        },
        950: {
            slidesPerView: 3,
        }
    },
    autoplay: {
        delay: 2500,
        disableOnInteraction: false,
    },
});
