$(document).ready( function () {
    var table = $('#servants_table').DataTable({
    dom: '<"top"lf>rt<"bottom"ip><"clear">',
    dom: '<"toolbar">f',
    order: [[6, 'asc']],
    pagingType: 'full_numbers',
    paging: false,
    responsive: true
    });

    var rarityIndex = getTableColumnIndex('Rarity');

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

function getTableColumnIndex(columnName) {
    columnIndex = 0;
    $("#servants_table th").each(function (i) {
        if ($($(this)).html() == columnName) {
          columnIndex = i; return false;
        }
      });
    return columnIndex;
};

function redrawTable() {
    $('#servants_table').DataTable().draw();
};

function getToggledServantRarities() {
    var values = []
    for (var i = 1; i < 6; i++) {
       var button = $('#rarityButton' + i)
       if (button.hasClass('active')) {
            values.push(button.val())
       }
    }
    return values
};

var rarityButtonClick = function()
{
    if (this.classList.contains('active')) {
        this.style.color = 'yellow'
    } else {
        this.style.color = 'grey'
    }
    $('#servants_table').DataTable().draw();
};


document.getElementById('rarityButton1').onclick = rarityButtonClick;
document.getElementById('rarityButton2').onclick = rarityButtonClick;
document.getElementById('rarityButton3').onclick = rarityButtonClick;
document.getElementById('rarityButton4').onclick = rarityButtonClick;
document.getElementById('rarityButton5').onclick = rarityButtonClick;

var classButtonClick = function()
{
    if (this.classList.contains('active')) {
        this.style.filter = 'grayscale(0) brightness(1)';
        this.style.border = 'none';
        this.style.background = 'none';
        this.style.boxShadow = 'none';
    } else {
        this.style.filter = 'grayscale(100) brightness(0.6)';
        this.style.border = 'none';
        this.style.background = 'none';
        this.style.boxShadow = 'none';
    }
};

document.getElementById('classButton1').onclick = classButtonClick;
document.getElementById('classButton2').onclick = classButtonClick;
document.getElementById('classButton3').onclick = classButtonClick;
document.getElementById('classButton4').onclick = classButtonClick;
document.getElementById('classButton5').onclick = classButtonClick;
document.getElementById('classButton6').onclick = classButtonClick;
document.getElementById('classButton7').onclick = classButtonClick;
document.getElementById('classButton8').onclick = classButtonClick;
document.getElementById('classButton9').onclick = classButtonClick;
document.getElementById('classButton10').onclick = classButtonClick;
document.getElementById('classButton11').onclick = classButtonClick;
document.getElementById('classButton12').onclick = classButtonClick;
document.getElementById('classButton13').onclick = classButtonClick;
document.getElementById('classButton14').onclick = classButtonClick;


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