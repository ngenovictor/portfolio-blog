(function($) {
    "use strict"; // Start of use strict

    // Smooth scrolling using jQuery easing
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: (target.offset().top - 48)
        }, 1000, "easeInOutExpo");
        return false;
      }
    }
    });

    // Highlight the top nav as scrolling occurs
    $('body').scrollspy({
        target: '.navbar-fixed-top',
        offset: 51,
    });

    // Closes responsive menu when a scroll trigger link is clicked
    $('.js-scroll-trigger').click(function() {
        $('.navbar-collapse').collapse('hide');
    });

    // Collapse the navbar when page is scrolled
    $(window).scroll(function() {
    if ($("#mainNav").offset().top > 100) {
      $("#mainNav").addClass("navbar-shrink");
    } else {
      $("#mainNav").removeClass("navbar-shrink");
    }
    });

    // Offset for Main Navigation
    $('#mainNav').affix({
        offset: {
            top: 100
        }
    })

    // Copy the email address to the clipboard and flash a "Copied!" note
    function copyText(text) {
        if (navigator.clipboard && window.isSecureContext) {
            return navigator.clipboard.writeText(text);
        }
        // Fallback for plain-http (local dev) and older browsers
        return new Promise(function(resolve, reject) {
            var $tmp = $("<textarea>").val(text).css({position: "fixed", opacity: 0}).appendTo("body");
            $tmp[0].select();
            var ok = document.execCommand("copy");
            $tmp.remove();
            ok ? resolve() : reject();
        });
    }

    $(".email-copy").on("click", function() {
        var $btn = $(this);
        var $toast = $btn.find(".email-copy-toast");
        copyText($btn.data("email")).then(function() {
            $toast.text("Copied!");
        }, function() {
            $toast.text("Copy failed");
        }).then(function() {
            $btn.addClass("copied");
            clearTimeout($btn.data("timer"));
            $btn.data("timer", setTimeout(function() {
                $btn.removeClass("copied");
            }, 1500));
        });
    });

})(jQuery); // End of use strict
