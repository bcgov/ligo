/* Project specific Javascript goes here. */

/*
Formatting hack to get around crispy-forms unfortunate hardcoding
in helpers.FormHelper:

    if template_pack == 'bootstrap4':
        grid_colum_matcher = re.compile('\w*col-(xs|sm|md|lg|xl)-\d+\w*')
        using_grid_layout = (grid_colum_matcher.match(self.label_class) or
                             grid_colum_matcher.match(self.field_class))
        if using_grid_layout:
            items['using_grid_layout'] = True

Issues with the above approach:

1. Fragile: Assumes Bootstrap 4's API doesn't change (it does)
2. Unforgiving: Doesn't allow for any variation in template design
3. Really Unforgiving: No way to override this behavior
4. Undocumented: No mention in the documentation, or it's too hard for me to find
*/
$('.form-group').removeClass('row');
$.fn.select2.defaults.set( "theme", "bootstrap" );

$(function () {
    $('[data-toggle="tooltip"]').tooltip();
});

// Mainly used for sorting Select2 drop-downs
var customSorter = function(data) {
    return data.sort(function (a, b) {
        return (a.text > b.text) ? 1 : (a.text < b.text) ? -1 : 0;
    });
}
