$(document).ready( function () {
    var table = $('#servants_table').DataTable({
    dom: '<"top"lf>rt<"bottom"ip><"clear">',
    dom: '<"toolbar">f',
    order: [[6, 'asc']],
    pagingType: 'full_numbers',
    paging: false,
    responsive: true
    });

    var rarityIndex = 0;
      $("#servants_table th").each(function (i) {
        if ($($(this)).html() == "Rarity") {
          rarityIndex = i; return false;
        }
      });

    $.fn.dataTable.ext.search.push(
        function (settings, data, dataIndex) {
          var rarities_toggled = getToggledServantRarities()
          var rarityColumn = data[rarityIndex];
          if (rarities_toggled.includes(rarityColumn)) {
            return true;
          }
          return false;
        }
      );
} );

function getToggledServantRarities() {
    var values = []
    for (var i = 1; i < 6; i++) {
       var button = $('#rarityButton' + i)
       if (button.hasClass('active')) {
            values.push(button.val())
       }
    }
    return values
}

var buttonClick = function()
{
    if (this.classList.contains('active')) {
        this.style.color = 'yellow'
    } else {
        this.style.color = 'grey'
    }
    $('#servants_table').DataTable().draw();
}

function redrawTable() {
    $('#servants_table').DataTable().draw();
};

document.getElementById('rarityButton1').onclick = buttonClick;
document.getElementById('rarityButton2').onclick = buttonClick;
document.getElementById('rarityButton3').onclick = buttonClick;
document.getElementById('rarityButton4').onclick = buttonClick;
document.getElementById('rarityButton5').onclick = buttonClick;

// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
     var forms = document.querySelectorAll('.needs-validation')
//    var forms = $("form");

    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }

                form.classList.add('was-validated');
            }, false)
        })
})()