function makeAjaxCall (url, data, callback) {
    $.ajax({
            type: 'POST',
            url: url,
            data: {...data, 
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()},
            dataType: 'json',
            success: callback,
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
            console.log(xhr, err, errmsg); // provide a bit more info about the error to the console
        }
    })
}

function handleCheck($, url, data) {
    makeAjaxCall(url, data, (json) => {
        if (json['movie_checked']) {
            $('.check-box').addClass('bi-check-square-fill watched-movie').removeClass('bi-check-square unwatched-movie');
            $('p.check-before-rating-message').remove();
        } else {
            $('.check-box').addClass('bi-check-square unwatched-movie').removeClass('bi-check-square-fill watched-movie');
            $('i.star').removeClass('active_star');
        }
    })
}

function handleManyChecks($, url, data, movie_pk) {
    var check_box_class = '.check-box-' + movie_pk
    makeAjaxCall(url, data, (json) => {
        if (json['movie_checked']) {
            $(check_box_class).addClass('bi-check-square-fill watched-movie').removeClass('bi-check-square unwatched-movie');
        } else {
            $(check_box_class).addClass('bi-check-square unwatched-movie').removeClass('bi-check-square-fill watched-movie');
        }
    })
}


function handleRating($, url, data) {
    makeAjaxCall(url, data, (json) => {
        // if user tries to rate movie before checking it, we display a message.
        if (! json['movie_checked']) {
            $("p.check-before-rating-message").remove();
            var message = $("<p class='check-before-rating-message'></p>").text("Check the movie before rating.");
            $(".error-message").append(message);
        } else {
            $("p.check-before-rating-message").remove();
            // making all the stars inactive when user clicks the maximum rated star.
            if (rating == -1) {
                $('i.active_star').removeClass('active_star');
            // user has clicked a star other than the maximum rated star.
            } else {
            const stars = document.querySelectorAll(".stars i");
            stars.forEach((star, index) => {
                    index <= rating ? star.classList.add("active_star") : star.classList.remove("active_star");
                })
            }
        }
    })
}

function handleAddToWatchList($, url, data) {
    makeAjaxCall(url, data, (json) => {
        if (json['in_watch_list']) {
            $('.plus').addClass('bi-plus-circle-fill watch-list-added').removeClass('bi-plus-circle watch-list-not-added');
        } else {
            $('.plus').addClass('bi-plus-circle watch-list-not-added').removeClass('bi-plus-circle-fill watch-list-added');
        }
    })
}
