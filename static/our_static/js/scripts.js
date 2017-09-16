(function($) {
    "use strict"; // Start of use strict

    // jQuery for page scrolling feature - requires jQuery Easing plugin
    $('.page-scroll a').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: ($($anchor.attr('href')).offset().top - 50)
        }, 1250, 'easeInOutExpo');
        event.preventDefault();
    });

    // Highlight the top nav as scrolling occurs
    $('body').scrollspy({
        target: '.navbar-fixed-top',
        offset: 51
    });

    // Closes the Responsive Menu on Menu Item Click
    $('.navbar-collapse ul li a').click(function(){ 
            $('.navbar-toggle:visible').click();
    });

    // Offset for Main Navigation
    $('#mainNav').affix({
        offset: {
            top: 100
        }
    })

    // Floating label headings for the contact form
    $(function() {
        $("body").on("input propertychange", ".floating-label-form-group", function(e) {
            $(this).toggleClass("floating-label-form-group-with-value", !!$(e.target).val());
        }).on("focus", ".floating-label-form-group", function() {
            $(this).addClass("floating-label-form-group-with-focus");
        }).on("blur", ".floating-label-form-group", function() {
            $(this).removeClass("floating-label-form-group-with-focus");
        });
    });

    //The contact form submit
    $(function() {
        $("form#contactForm").submit(function (event) {
            event.preventDefault();
            var name = $("input#name").val();
            var emailAddress = $("input#email").val();
            var message = $("textarea#message").val();
            var csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
            var data = {
                "name":name,
                "email_address":emailAddress,
                "message":message,
                "csrfmiddlewaretoken":csrfmiddlewaretoken
            }

            $.ajax({
                method:"POST",
                url:"/contact",
                data:data,
                success:function(message){
                    if(message["message"] == "success"){
                        $("input#name").val("");
                        $("input#email").val("");
                        $("textarea#message").val("");
                        $("p#contact_message").text("Thank you for contacting me. Your message has been received. I will be sure to get back to you as soon as I can");
                        $("#message_send_feedback").modal("show");
                    }else if(message["message"] == "error"){
                        $("p#contact_message").text("Something went wrong. Please ensure that you have filled all the inputs and try again!!");
                        $("#message_send_feedback").modal("show");
                    }else{
                        $("p#contact_message").text("");
                        $("p#contact_message").append("Thank you for contacting me. There was an error on our side. Please contact me on <a href='mailto:ngenovictor321@gmail.com'>Email</a>");
                        $("#message_send_feedback").modal("show");
                    }

                    console.log(message);
                }
            });
        });
    });

})(jQuery); // End of use strict