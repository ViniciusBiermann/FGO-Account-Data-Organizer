$('#month').on('change', function() {
    selectedMonth = this.value;
    days = 31;
    if (['4', '6', '9'].includes(selectedMonth)) {
       days = 30;
    }
    if (selectedMonth == 2) {
       days = 29;
    }

    var opts = [];
    for (var i = 1; i <= days; i++) {
        opts.push($('<option />', {
            text: i,
            value: i
        }));
    }
    $('#day').html(opts);
}).trigger('change');