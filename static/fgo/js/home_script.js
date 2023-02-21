$(document).ready( function () {
    var table = $('#servants_table').DataTable({
    dom: '<"top"lf>rt<"bottom"ip><"clear">',
    dom: '<"toolbar">f',
    order: [[8, 'asc']],
    pagingType: 'full_numbers',
    paging: false,
    responsive: true
    });

    var rarityIndex = getTableColumnIndex('Rarity');
    var servantClassIndex = getTableColumnIndex('Class');

    $.fn.dataTable.ext.search.push(
        function (settings, data, dataIndex) {
          var rarities_toggled = getToggledServantRarities();
          var rarityColumn = data[rarityIndex];
          var classesToggled = getToggledServantClasses();
          var classColumn = data[servantClassIndex];
          if (rarities_toggled.includes(rarityColumn) && classesToggled.includes(classColumn)) {
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

function getToggledServantClasses() {
    var values = []
    for (var i = 1; i < 15; i++) {
       var button = $('#classButton' + i)
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
    $('#servants_table').DataTable().draw();
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


function changeCurrentMasterInfo(masterInfo) {
    $('#masterName').html(masterInfo.name);
    $('#masterID').html(masterInfo.in_game_id);
    $('#masterLevel').html(masterInfo.master_level);
    $('#masterBDay').html(masterInfo.birthday);
    $('#masterGender').html(masterInfo.gender);
    $('#masterLogins').html(masterInfo.total_logins);
    $('#masterDevice').html(masterInfo.device);
    $('#masterDownloadDate').html(masterInfo.download_date);
    $('#masterLastAccess').html(masterInfo.last_access);
    $('#masterSQ').html(masterInfo.saint_quartz);
    $('#masterPaidSQ').html(masterInfo.paid_saint_quartz);
    $('#masterRarePrisms').html(masterInfo.rare_prisms);
    $('#masterManaPrisms').html(masterInfo.mana_prisms);
    $('#masterUnregisteredSpiritOrigin').html(masterInfo.unregistered_spirit_origin);
    $('#masterRecoveryNumber').html(masterInfo.recovery_number);
}

function changeServantTableBody(servants_list) {
    var table = $('#servants_table').DataTable();
    table.clear();
    servants_list.forEach(function(servant){
        let common_data = servant.servant_data;
        table.row.add(
            [common_data.id, common_data.name, common_data.servant_class, '★'.repeat(common_data.rarity), servant.level,
            servant.bond_level, servant.np_level,
            servant.skill_1_level + '-' + servant.skill_2_level + '-' + servant.skill_3_level, servant.summon_date,
            '<button onclick="window.location.href=' + "'#'\"" + " type='button' class='btn btn-sm btn-info'>Edit</button>"]
        )
    });
    table.draw()
};

$('#mastersSelect').on('change', function() {
    selectedMaster = this.value;
    fetch('http://127.0.0.1:8000/masters/' + selectedMaster)
    .then((response) => response.json())
    .then((data) => changeCurrentMasterInfo(data));

    fetch('http://127.0.0.1:8000/masters/' + selectedMaster + '/servants')
    .then((response) => response.json())
    .then((data) => changeServantTableBody(data));
}).trigger('change');
