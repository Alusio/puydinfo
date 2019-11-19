(function ($) {
    "use strict"

    // Mobile dropdown
    $('.has-dropdown>a').on('click', function () {
        $(this).parent().toggleClass('active');
    });

    // Aside Nav
    $(document).click(function (event) {
        if (!$(event.target).closest($('#nav-aside')).length) {
            if ($('#nav-aside').hasClass('active')) {
                $('#nav-aside').removeClass('active');
                $('#nav').removeClass('shadow-active');
            } else {
                if ($(event.target).closest('.aside-btn').length) {
                    $('#nav-aside').addClass('active');
                    $('#nav').addClass('shadow-active');
                }
            }
        }
    });

    $('.nav-aside-close').on('click', function () {
        $('#nav-aside').removeClass('active');
        $('#nav').removeClass('shadow-active');
    });


    $('.search-btn').on('click', function () {
        $('#nav-search').toggleClass('active');
    });

    $('.search-close').on('click', function () {
        $('#nav-search').removeClass('active');
    });

})(jQuery);

document.body.addEventListener("touchstart", startTouch, false);
document.body.addEventListener("touchmove", moveTouch, false);

// Swipe Up / Down / Left / Right
var initialX = null;
var initialY = null;

function startTouch(e) {
    initialX = e.touches[0].clientX;
    initialY = e.touches[0].clientY;
};

function moveTouch(e) {
    if (initialX === null) {
        return;
    }

    if (initialY === null) {
        return;
    }

    var currentX = e.touches[0].clientX;
    var currentY = e.touches[0].clientY;

    var diffX = initialX - currentX;
    var diffY = initialY - currentY;

    if (Math.abs(diffX) > Math.abs(diffY)) {
        // sliding horizontally
        if (diffX > 0) {
            // swiped left
            $('#nav-aside').removeClass('active');
            $('#nav').removeClass('shadow-active');
        } else {
            // swiped right
            $('#nav-aside').addClass('active');
            $('#nav').addClass('shadow-active');
        }
    } else {
        // sliding vertically
        if (diffY > 0) {
            // swiped up

        } else {
            // swiped down

        }
    }

    initialX = null;
    initialY = null;

};
