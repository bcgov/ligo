$(function () {
    $.ajaxSetup({
        headers: { "X-CSRFToken": Cookies.get('csrftoken') }
    });
    $('select').select2();
});

function preview() {
    var processResponse = function(response_data, textStatus_ignored, jqXHR_ignored)  {
        $('#preview-container').html(response_data);
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


$('#preview-form').on('submit', function(event){
    event.preventDefault();
    preview();
});
