$(document).ready(function () {
    $('.bx-vertical').bxSlider({
        minSlides: 2,
        maxSlides: 2,
        slideWidth: 360,
        slideMargin: 10,
        slideHeight: 175,
        pager: true,
        ticker: true,
        speed: 35000,
        tickerHover: true,
        useCSS: false,
        mode: 'vertical'
    });

    $('.bx-horizontal').bxSlider({
        minSlides: 2,
        maxSlides: 5,
        slideWidth: 300,
        slideMargin: 10,
        pager: false,
        ticker: true,
        speed: 35000,
        tickerHover: true,
        useCSS: false
    });

    $('.bx-horizontal-click').bxSlider({
        minSlides: 2,
        maxSlides: 5,
        slideWidth: 300,
        slideMargin: 10
    });
});

