$(document).ajaxStart(function() { $('#loading').show();});
$(document).ajaxComplete(function() { $('#loading').hide(); });
$(document).ajaxError(function() { $('#loading').hide(); });


function isNumberKey(e){
  // Allow: backspace, delete, tab, escape, enter and .
    if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
      // Allow: Ctrl+A,Ctrl+C,Ctrl+V, Command+A
      ((e.keyCode == 65 || e.keyCode == 86 || e.keyCode == 67 || e.keyCode == 88 || e.keyCode == 90 || e.keyCode == 89) && (e.ctrlKey === true || e.metaKey === true)) ||
      // Allow: home, end, left, right, down, up
      (e.keyCode >= 35 && e.keyCode <= 40)) {
      // let it happen, don't do anything
      return;
    }
    
    
    // Ensure that it is a number and stop the keypress
    if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
      e.preventDefault();
    }
};

function isPhoneKey(e){
  // Allow: backspace, delete, tab, escape, enter and .
    if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110]) !== -1 ||
      // Allow: Ctrl+A,Ctrl+C,Ctrl+V, Command+A
      ((e.keyCode == 65 || e.keyCode == 86 || e.keyCode == 67 || e.keyCode == 88 || e.keyCode == 90 || e.keyCode == 89) && (e.ctrlKey === true || e.metaKey === true)) ||
      // Allow: home, end, left, right, down, up
      (e.keyCode >= 35 && e.keyCode <= 40)) {
      // let it happen, don't do anything
      return;
    }
    
    
    // Ensure that it is a number and stop the keypress
    if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
      e.preventDefault();
    }
};

// ajaxStart(function() { run(); });

// function run(){
//   console.log('ss')
// }


if ($('#msg_pesan').length){
  msg_pesan($("#msg_pesan").attr('data'),$("#msg_pesan").attr('alt'));
}

function msg_pesan(meseg,jenis_icon){
    toastr.options = {
      "closeButton": false,
      "debug": false,
      "newestOnTop": false,
      "progressBar": false,
      "positionClass": "toast-top-right",
      "preventDuplicates": false,
      "onclick": null,
      "showDuration": "300",
      "hideDuration": "1000",
      "timeOut": "5000",
      "extendedTimeOut": "1000",
      "showEasing": "swing",
      "hideEasing": "linear",
      "showMethod": "fadeIn",
      "hideMethod": "fadeOut"
    }

  toastr[jenis_icon](meseg)
}

function showModal(e,modal,act = 'add'){
  var url_load  = "";
  var loadModal = "";
  var linkLoad  = $(e).attr('alt');
  
  switch(modal) {
    case "peserta_didik":
        if(act == "add"){
          loadModal = "Tambah Siswa Baru";
        } else if(act == "edit"){
          loadModal = "Edit Siswa";
        }
        url_load  = linkLoad;
        break;

    case "list_ujian":
        if(act == "add"){
          loadModal = "Tambah Ujian Baru";
        } else if(act == "edit"){
          loadModal = "Edit Ujian";
        }
        url_load  = linkLoad;
        break;

    case "profil_peserta_didik":
        if(act == "edit"){
          loadModal = "Profil";
        }
        url_load  = linkLoad;
        break;

    case "profil_guru":
        if(act == "edit"){
          loadModal = "Profil Guru";
        }
        url_load  = linkLoad;
        break;

    case "sett":
        loadModal = "Setting Aplikasi";
        url_load  = linkLoad;
        break;

    case "guru":
        if(act == "add"){
          loadModal = "Tambah Guru Baru";
        } else if(act == "edit"){
          loadModal = "Edit Guru";
        }
        url_load  = linkLoad;
        break;
    }
  document.getElementById("myModalLabel").innerHTML = loadModal;
  $("#showModal").modal();
  $(".modal-body-showmodal").load(url_load);
  $(".modal-dialog2").css('width', '1200px');
};