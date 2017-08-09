function getDataTypesJson() {
    var d_types = {};
    $('.data-type').each(function() {
        var field_name = $(this).attr('id').slice(0, -6);
        var field_type = $(this).val();
        d_types[field_name] = field_type;
    });
    return JSON.stringify(d_types)

}

function getFieldCatsJson() {
    var field_cats = {};
    $('.field-cat').each(function() {
        var field_name = $(this).attr('id').slice(0, -4);
        var field_cat = $(this).val();
        field_cats[field_name] = field_cat;
    });
    console.log(field_cats);
    return JSON.stringify(field_cats)
}

$("#dataset-form").submit(function() {
    $("#id_data_types").val(getDataTypesJson());
    $("#id_field_cats").val(getFieldCatsJson());
    return true;

});

$(function () {
    data_types = data_types || {};
    $('.data-type').each(function() {
        var field_name = $(this).attr('id').slice(0, -6);
        var field_type = data_types[field_name] || header_types[field_name];
        $(this).val(field_type);
    });
    field_cats = field_cats || {};
    //console.log(field_cats);
    $('.field-cat').each(function() {
        var field_name = $(this).attr('id').slice(0, -4);
        var field_type = field_cats[field_name];
        $(this).val(field_type);
    });
    $('select').select2({
        width: 'none',
        sorter: customSorter
    });
});
