
$('.project-exec').on('click', function() {
    var view_link = $(this).parent().find('.results-view');
    view_link.hide();
    var exec_link = $(this).parent().find('.project-exec');
    exec_link.hide();
    $(this).parent().parent().find('.status-cell').text('RUNNING');
});


var task_timer = null;

$(function () {
    $.ajaxSetup({
        headers: { "X-CSRFToken": Cookies.get('csrftoken') }
    });
    checkStatus(total_running);
    $('[data-toggle="tooltip"]').tooltip();
});

var updateStatus = function() {
    var processResponse = function(response_data, textStatus_ignored, jqXHR_ignored)  {
        $('.projects-container').html(response_data);
        checkStatus(parseInt(total_running));
    };
    var list_req = {
        url : STATUS_URL ,
        type : "GET",
        success: processResponse
    };
    $.ajax(list_req);
};

function checkStatus( total) {
    if (total > 0) {
        console.log("Total tasks running: " + total);
        if (task_timer != null) return;
        task_timer = setInterval(updateStatus, 10000)
    }
    else {
        console.log("No tasks are running at the moment.");
        clearInterval(task_timer);
        task_timer = null;
    }
}

