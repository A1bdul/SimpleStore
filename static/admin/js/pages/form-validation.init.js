!function () {
    "use strict";
    window.addEventListener("load", function () {
        var t = document.getElementsByClassName("needs-validation");
        Array.prototype.filter.call(t, function (e) {
            e.addEventListener("submit", function (t) {
                !1 === e.checkValidity() && (t.preventDefault(), t.stopPropagation()), e.classList.add("was-validated")
            }, !1)
        })
    }, !1)
}(), $(document).ready(function () {
    $(".custom-validation").parsley()
});

/*
 * Used to validate a form with parsley
 * Add jquery and parsley plugin before this script block
 * Add class validated-form to the form
 * Add class 'ajax-parsley-form' to the ajax form
 *
**/

var parsleyForm = $('.validated-form').parsley({
    errorsWrapper: '<span class="help-block"></span>',
    errorTemplate: '<small></small>'
});
window.Parsley.on('field:error', function () {
    this.$element.parents('.form-group').addClass('has-error');
});
window.Parsley.on('field:success', function () {
    this.$element.parents('.form-group').removeClass('has-error');
});
window.Parsley.on('form:error', function () {
    $('html, body').animate({
        scrollTop: $('body').offset().top
    }, 300);
});

$(function () {
    $('.ajax-parsley-form button[type=submit]').bind('click', function (e) {
        e.preventDefault();

        if (parsleyForm.isValid()) {
            //if (parsleyForm.validate()) {
            var form = $('.validated-form');
            $.post(form.attr('action'), form.serialize(), function (response) {
                console.log(response);
            });
        }
    });
});