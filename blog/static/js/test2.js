!function (a) {
    "function" == typeof define && define.amd ? define(["jquery", "./version", "./focusable"], a) : a(jQuery)
}(function (a) {
    return a.extend(a.expr[":"], {
        tabbable: function (b) {
            var c = a.attr(b, "tabindex"), d = null != c;
            return (!d || c >= 0) && a.ui.focusable(b, d)
        }
    })
})