$(function() {
    $.ajaxSetup({
        headers: { "X-CSRFToken": Cookies.get('csrftoken') }
    });
    $('select').select2();

    // Mirror horizontal scrolling between top and bottom bars
    $("#preview-table-topscroll").scroll(function() {
        $("#preview-table").scrollLeft($("#preview-table-topscroll").scrollLeft());
    });
    $("#preview-table").scroll(function() {
        $("#preview-table-topscroll").scrollLeft($("#preview-table").scrollLeft());
    });
});

$('#preview-form').on('submit', function(event){
    event.preventDefault();
    preview();
});

function preview() {
    var processResponse = function(response_data, textStatus_ignored, jqXHR_ignored) {
        $('.preview-data').html(response_data);
    }
    var preview_req = {
        url : PREVIEW_URL + "preview/",
        type : "POST",
        data : {
            dataset: dataset_name,
            filename: filename,
            limit : $('#preview_size').val(),
            criteria : $('#rows_select').val(),
        },
        success: processResponse
    };
    $.ajax(preview_req);
};
