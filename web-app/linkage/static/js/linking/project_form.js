var left_header = [];
var right_header = [];
var status = 'DRAFT';

$(document).ready(function() {
    $.ajaxSetup({
        headers: { "X-CSRFToken": Cookies.get('csrftoken') }
    });

    getLeftHeader();
    if (project_type === 'LINK') {
        getRightHeader();
    }
    var total_steps = $("#id_steps-TOTAL_FORMS").val();
    $("#form-steps-container input:checkbox").hide();

    $('.step-seq').each(function(index) {
        $(this).val(index + 1);
    });
    $('select').select2({width: 'none'});

    $('#form-steps-container .blocking-vars .alg').select2({
        width: 'none',
        placeholder: "Please select a transformation"
    });

    $('#form-steps-container .linking-vars .alg').select2({
        width: 'none',
        placeholder: "Please select a comparison method"
    });

    // Disable tab links
    $("#project-tabs > li").click(function() {
        if($(this).hasClass("disabled"))
            return false;
    });

    // Jump to specified tab from hash
    var hash = window.location.hash;
    if (hash != "")
        $('#project-tabs a[href="' + hash + '"]').tab('show');
    else
        $('#project-tabs a:first').tab('show');

    showProjectTitle();
    tabDisableState();
    saveButtonState();
    createContinueButtonState();
});

// Update button visibility on tab change
$(document).on('shown.bs.tab', 'a[data-toggle="tab"]', function() {
    showProjectTitle();
    tabDisableState();
    createContinueButtonState();
})

// Continue button functionality
$("#step-continue").click(function() {
    var tab = $("#project-tab-content > .active").attr("id");
    if (tab === "project-main-tab" || tab === "project-steps")
        $('#project-tabs > .active').next('li').find('a').trigger('click');
});

// Tab flow - disable functionality
function tabDisableState() {
    var stepsTab = $("#tab-steps");
    var resultsTab = $("#tab-results");
    var tab = $("#project-tab-content > .active").attr("id");

    switch(tab) {
        case "project-main-tab":
            ($("#step-create").length > 0) ? stepsTab.removeClass("disabled") : stepsTab.addClass("disabled");
        case "project-steps":
            ($("#id_steps-TOTAL_FORMS").val() > 0) ? resultsTab.removeClass("disabled") : resultsTab.addClass("disabled");
            break;
        case "project-results":
            stepsTab.removeClass("disabled");
            resultsTab.removeClass("disabled");
            break;
        default:
            break;
    }
}

// Save button visibility
function saveButtonState() {
    var saveBtn = $("#project-save");
    ($("#step-create").length > 0 && $("#id_steps-TOTAL_FORMS").val() > 0) ? saveBtn.removeClass("hidden") : saveBtn.addClass("hidden");
}

// Create, Continue button visibility
function createContinueButtonState() {
    if ($("#project-save").hasClass("hidden")) {
        var createBtn = $("#project-create");
        var contBtn = $("#step-continue");
        var tab = $("#project-tab-content > .active").attr("id");

        switch(tab) {
            case "project-main-tab":
                if ($("#step-create").length > 0) {
                    createBtn.addClass("hidden");
                    contBtn.removeClass("hidden disabled");
                } else {
                    createBtn.removeClass("hidden");
                    contBtn.addClass("hidden disabled");
                }
                break;
            case "project-steps":
                createBtn.addClass("hidden");
                contBtn.removeClass("hidden");
                ($("#id_steps-TOTAL_FORMS").val() > 0) ? contBtn.removeClass("disabled") : contBtn.addClass("disabled");
                break;
            case "project-results":
                createBtn.addClass("hidden disabled");
                contBtn.addClass("hidden");
                saveButtonState();
                break;
            default:
                createBtn.addClass("hidden disabled");
                contBtn.addClass("hidden");
                break;
        }
    }
}

// Display project title on steps and results tab
function showProjectTitle() {
    var title = $('#id_name').val();
    var projTitle = $('#project-title');
    var tab = $("#project-tab-content > .active").attr("id");

    projTitle.text(title);
    (title !== "" && tab === "project-steps" || tab === "project-results") ? projTitle.removeClass("hidden") : projTitle.addClass("hidden");
}

function getLeftHeader() {
    var selectedDataset = $('#id_left_data').find("option:selected").val();
    if (selectedDataset) {
        var leftDataset = $('#id_left_data').find("option:selected").text();
        $('#left-columns-title').text(leftDataset + ' Columns:');
        getHeader(left_data_id, 'left-header', function(header) {
            left_header = header;
        });
    }
}

function getRightHeader() {
    var selectedDataset = $('#id_right_data').find("option:selected").val();
    if (selectedDataset) {
        var rightDataset = $('#id_right_data').find("option:selected").text();
        $('#right-columns-title').text(rightDataset + ' Columns:');
        getHeader(right_data_id, 'right-header', function(header) {
            right_header = header;
        });
    }
}

function getHeader(elmnt, class_name, callback) {
    if (typeof elmnt === 'undefined') return;

    var dataset_id = $("#" + elmnt).val();
    var processResponse = function(response_data, textStatus_ignored, jqXHR_ignored)  {
        var header =  response_data.header;
        var options = '<option value=""></option>';
        for (i=0; i < header.length; i++) {
            options += '<option value="' + header[i] + '">' + header[i] + '</option>';
        }

        header_options[elmnt] = options;

        $('.' + class_name).each(function() {
            var selected_val = $(this).val();
            $(this).html(options);
            $(this).val(selected_val);
        });

        return header;
    };
    var data_header_req = {
        url : DATASET_COLUMNS_URL ,
        type : "GET",
        data : {
            id: dataset_id,
        }
    };
    $.ajax(data_header_req).done(
        function(response) {
            var header = processResponse(response);
            if (typeof callback !== 'undefined') {
                callback(header);
            }
        }
    );
}

$("#" + left_data_id).change(function() {
    getLeftHeader();
});

function showSelectedColumns(header, columns, requiredCols) {
    var columnsHtml = '';

    for (var index = 0; index < header.length; index++) {
        var item = header[index];
        var colHtml = '<div class="col-sm-4"><input type="checkbox" value="' + item + '"';
        if (columns && columns.indexOf(item) != -1) {
            colHtml += 'Checked="Checked" ';
        }
        if (requiredCols && requiredCols.indexOf(item) != -1) {
            colHtml += 'disabled="true" ';
        }
        colHtml += '>&nbsp;<span>' + item +'</span></div>';
        columnsHtml += colHtml;
    }

    return columnsHtml;
}

function getVariable(typeSelector, headerSelector, index) {
    var selector = '#' + typeSelector + '-vars-' + index + ' .' + headerSelector;
    var items = [];
    $(selector).not(".deleted").each(function() {
        var selected_val = $(this).val();
        items.push(selected_val);
    });

    return items;
}

function blocking_json(index) {
    schema = {left : [], right: [], transformations: [] };

    schema.left = getVariable('blocking', 'left-blocking-var', index);
    schema.right = getVariable('blocking', 'right-blocking-var', index);

    if (schema.left.length == 0) {
        status = 'DRAFT';
    }

    var trans_selector = "#blocking-vars-" + index + " .alg";
    $(trans_selector).not(".deleted").each(function() {
        var selected_val = $(this).val();
        if (!selected_val.trim()) {
            status ='DRAFT';
        }
        schema.transformations.push(selected_val);
    });

    for (var index=0; index < schema.left.length; index++) {
        if (!schema.left[index].trim()) {
            status = 'DRAFT';
        }
        if (project_type == 'LINK' && !schema.right[index].trim()) {
            status = 'DRAFT'
        }
    }

    return JSON.stringify(schema);
}

function linking_json(index) {
    schema = {left : [], right: [], comparisons: [] };
    schema.left = getVariable('linking', 'left-link-var', index);
    schema.right = getVariable('linking', 'right-link-var', index);

    if (schema.left.length == 0) {
        status = 'DRAFT';
    }

    var link_method = $('#id_steps-' + index + '-linking_method').val();
    var trans_selector = "#linking-vars-" + index + " .alg";
    $(trans_selector).not(".deleted").each(function() {
        var selected_val = $(this).val();
        if (!selected_val.trim()) {
            status = 'DRAFT';
        }
        var suffix = this.id.slice(9);

        var comparison = {"name": selected_val};
        args_list = COMPARISON_ARGS[link_method][selected_val];
        if (args_list) {
            args = {};
            for (index = 0; index < args_list.length; index++) {
                arg = {};
                arg_id = "link_comp_arg" + suffix + "_" + index;
                var arg_val = $("#" + arg_id).val();
                var arg_name = $('label[for="' + arg_id + '"]').html();
                if (!arg_val.trim()) {
                    status = 'DRAFT';
                }
                else {
                    arg_val = (!isNaN(arg_val)) ? parseFloat(arg_val) : arg_val;
                }
                args[arg_name] = arg_val;
            }
            comparison["args"] = args;
        }
        schema.comparisons.push(comparison);
    });


    for (var index=0; index < schema.left.length; index++) {
        if (!schema.left[index].trim()) {
            status = 'DRAFT';
        }
        if (project_type == 'LINK' && !schema.right[index].trim()) {
            status = 'DRAFT'
        }
    }

    return JSON.stringify(schema);
}

function getSelectedColumns(selector) {

    columns = [];
    selector.find('input:checkbox').each(function() {
        if ($(this).prop('checked')) {
            columns.push($(this).val());
        }
    });
    return columns;
}

$("#linking-form").submit(function() {
    status = 'READY';
    var left_vars = [];
    var right_vars = [];
    var count = parseInt($('#id_steps-TOTAL_FORMS').val());
    //Reconstruct blocking and linking schema from the input elements
    for (var index = 0; index <count; index++) {

        var field_select = "#id_steps-" + index + "-blocking_schema";
        $(field_select).val(blocking_json(index));

        field_select = "#id_steps-" + index + "-linking_schema";
        $(field_select).val(linking_json(index));

        left_vars = left_vars.concat(getVariable('blocking', 'left-header', index));
        left_vars = left_vars.concat(getVariable('linking', 'left-header', index));
        right_vars = right_vars.concat(getVariable('blocking', 'right-header', index));
        right_vars = right_vars.concat(getVariable('linking', 'right-header', index));
    }

    left_vars = left_vars.concat(required_left);
    leftColumns = getSelectedColumns($('#selected_left_columns'));
    for (index in left_vars) {
        if (left_vars[index] && leftColumns.indexOf(left_vars[index]) == -1) {
            leftColumns.push(left_vars[index]);
        }
    }

    $('#id_left_columns').val(JSON.stringify(leftColumns));
    if (project_type == 'LINK') {
        right_vars = right_vars.concat(required_right);
        rightColumns = getSelectedColumns($('#selected_right_columns'));
        for (index in right_vars) {
            if (right_vars[index] && rightColumns.indexOf(right_vars[index]) == -1) {
                rightColumns.push(right_vars[index]);
            }
        }
        $('#id_right_columns').val(JSON.stringify(rightColumns));
    }

    if (!count || count == 0) {
        status = 'DRAFT'
    }

    $('#id_status').val(status);
    return true;
});

$('#form-steps-container').on('click', '.blocking-vars .blocking-var-remove', function() {
    var row = $(this).parent().parent().parent().parent().parent();
    row.find("select, input").addClass( "deleted" );
    row.hide();

    return false;
});

$('#form-steps-container').on('click', '.linking-vars .linking-var-remove', function() {
    var row = $(this).parent().parent().parent().parent().parent();
    row.find("select, input").addClass( "deleted" );
    row.hide();

    return false;
});

$("#form-steps-container").on('change', '.link-vars-container .link-var-row .alg', function(){
    var select_id = $(this).attr('id');
    var form_index = select_id.slice(10).split('_')[0];
    var step_link_method = $('#id_steps-' + form_index + '-linking_method').val();
    suffix = select_id.slice(9);
    var selected_alg = $(this).val();
    $(this).parent().parent().parent().find('.alg-arg').empty();
    var args_list = comparison_args[step_link_method][selected_alg];
    if (args_list) {
        args_html = '';
        for (index = 0; index < args_list.length; index++) {
            arg_id = 'link_comp_arg' + suffix + '_' + index;
            arg_name = args_list[index];
            args_html += '<label for="' + arg_id + '" class="control-label col-sm-2">' + arg_name + '</label>'
                    + '<div class="preview col-sm-4"><input id="' + arg_id + '" type="text" class="form-control"></div>';
        }
        $(this).parent().parent().parent().find('.alg-arg').append(args_html);
    }

});

$("#form-steps-container").on('change', '.link-method', function() {
    var selected_method = $(this).val()
    var form_id = $(this).parent().parent().parent().parent().attr('id');
    var form_index = form_id.slice(-1);

    //Find the selected linking method
    var step_link_method = $('#id_steps-' + form_index + '-linking_method').val();

    //Fetch the list of comparison algorithms for the selected linking method.
    var cmprsnChoices = comparison_choices[step_link_method];

    //Refresh the list of comparison algorithms for all drop down list of this step.
    var comparisons = '<option value=""></option>';
    for (item in cmprsnChoices) {
        comparisons += '<option value="' + cmprsnChoices[item][0] + '">' + cmprsnChoices[item][1] + '</option>';
    }

    //Remove input elements of parameters of previously selected algorithms.
    $('#' + form_id + ' .link-var-row .alg').each(function(index) {
        $(this).html(comparisons);
    });
    $('#' + form_id + ' .link-var-row .alg-arg').each(function(index) {
        $(this).empty();
    });
});

$("#form-steps-container").on('click', '.step-delete', function() {
    var form_id = $(this).parent().parent().attr('id');
    var form_index = form_id.slice(10);
    var delete_id = "id_steps-" + form_index + "-DELETE" ;
    $("#" + delete_id).prop('checked', true);
    $("#" + form_id).hide();
    return false;
});

/*
    Based on the stackoverflow solution provided here :
    http://stackoverflow.com/questions/21260987/add-a-dynamic-form-to-a-django-formset-using-javascript-in-a-right-way?answertab=votes#tab-top
 */
$("#step-create").click(function() {
    var count = parseInt($('#id_steps-TOTAL_FORMS').val());
    var tmplMarkup = $('#item-template').html();
    var compiledTmpl = tmplMarkup.replace(/__prefix__/g, count);
    $('div#form-steps-container').append(compiledTmpl);

    $('#id_steps-TOTAL_FORMS').val(count+1);
    $("#id_steps-" + count +"-DELETE").hide();
    $("#id_steps-" + count +"-seq").val(count+1);

    $('#form-step-' + count + ' .link-method').select2({width: 'none'});

    tabDisableState();
    createContinueButtonState();
    return false
});

$('a[href="#project-results"]').on('click', function() {
    var left_vars = [];
    var right_vars = [];

    var count = parseInt($('#id_steps-TOTAL_FORMS').val());
    for (var index = 0; index <count; index++) {
        left_vars = left_vars.concat(getVariable('blocking', 'left-header', index));
        left_vars = left_vars.concat(getVariable('linking', 'left-header', index));
        right_vars = right_vars.concat(getVariable('blocking', 'right-header', index));
        right_vars = right_vars.concat(getVariable('linking', 'right-header', index));
    }

    for (index in left_vars) {
        if (left_vars[index] && leftColumns.indexOf(left_vars[index]) == -1) {
            leftColumns.push(left_vars[index]);
        }
    }

    for (index in right_vars) {
        if (right_vars[index] && rightColumns.indexOf(right_vars[index]) == -1) {
            rightColumns.push(right_vars[index]);
        }
    }

    var columnsHtml = showSelectedColumns(left_header, leftColumns, left_vars.concat(required_left));
    $('#selected_left_columns').html(columnsHtml);

    if (project_type == 'LINK') {
        columnsHtml = showSelectedColumns(right_header, rightColumns, right_vars.concat(required_right));
        $('#selected_right_columns').html(columnsHtml);
    }

});

function updateSelectedColumns(columnSet, selectedElem) {
    var value = selectedElem.val();
    if (selectedElem.prop('checked')) {
        columnSet.push(value);
    }
    else {
        var index = columnSet.indexOf(value);
        if (index > -1) {
            columnSet.splice(index, 1);
        }
    }
}

$('#selected_left_columns').on('click', ' input:checkbox', function() {
    updateSelectedColumns(leftColumns, $(this));
});

$('#selected_right_columns').on('click', ' input:checkbox', function() {
    updateSelectedColumns(rightColumns, $(this));
});


var previous_link_var;
var previous_block_var;


$("#form-steps-container").on('select2:selecting', '.link-vars-container .link-var-row .left-link-var', function(){
    // Store the left variable before the change.
    previous_link_var = this.value;

});

$("#form-steps-container").on('select2:select', '.link-vars-container .link-var-row .left-link-var', function(){
    if (project_type === 'LINK')  return;

    var left_var_id = $(this).attr('id');
    var right_var_id = 'link_id_right' + left_var_id.slice(12);

    var right_selected_value = $('#' + right_var_id).val();

    // Change the right variable to the new value if left and right variables were the same before the change.
    if (previous_link_var === right_selected_value) {
        $('#' + right_var_id).val($(this).val());
        $('#' + right_var_id).select2({width: 'none'});
    }
});


$("#form-steps-container").on('select2:selecting', '.block-vars-container .block-var-row .left-blocking-var', function() {
    // Store the left variable before the change.
    previous_block_var = this.value;

});

$("#form-steps-container").on('select2:select', '.block-vars-container .block-var-row .left-blocking-var', function(){
    if (project_type === 'LINK')  return;

    var left_var_id = $(this).attr('id');
    var right_var_id = 'block_id_right' + left_var_id.slice(13);

    var right_selected_value = $('#' + right_var_id).val();

    // Change the right variable to the new value if left and right variables were the same before the change.
    if (previous_block_var === right_selected_value) {
        $('#' + right_var_id).val($(this).val());
        $('#' + right_var_id).select2({width: 'none'});
    }
});
