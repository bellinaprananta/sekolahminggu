$(document).ready(function(){
		$('#table_user').DataTable( {
		dom: 'Bfrtip',
		buttons: [
			'excel', 'pdf'
		]
	} );

		
	})

	function edit_user(e){
		$.ajax({
            type: "GET",
            // headers: { "X-CSRFToken": csrf_token },
            url: $(e).attr('edit_url'),
            data: {'uid':$(e).attr('data-id')},
            dataType: 'json',
            success: function(res){
                if (res['level'] == 'SISWA') {
                    msg_pesan('Silahkan Edit Melalui Menu Kesiswaan > Peserta Didik.', 'error')
                }else if(res['level'] == 'GURU'){
                    msg_pesan('Silahkan Edit Melalui Menu Guru.', 'error')
                }else{
                	data = res['data_user'][0];
                	$('#id_nip').val(data['nip']);
                	$('#id_fullname').val(data['fullname']);
                	$('#select_hakakses').val(data['level']);
                	$('#select_hakakses').val(data['level']);
                	$('#id_uname').val(data['uname']);
                	$('#id_pwd').val('ss');
                	$('#div_pwd').css('display', 'none');
                	$('#cancel_edit').css('display', '');
                	$('#frm_user').attr('action', $(e).attr('edit_url'))
                }
            },
            error: function(res){
                msg_pesan('Hapus Item Gagal. ','error');
                $('#frm_user').attr('action', "{% url 'bimbel_app:usermanagement' %}");
                $('#cancel_edit').css('display', 'none');
            }
        });
	};

	function delete_user(e){
        Swal.fire({
                  title: 'Yakin mau menghapus User \"'+$(e).attr('data-u')+'\" ?',
                  icon: 'warning',
                  showCancelButton: true,
                  confirmButtonColor: '#3085d6',
                  cancelButtonColor: '#d33',
                  confirmButtonText: 'Hapus'
                }).then((result) => {
                  if (result.isConfirmed) {
                    $.ajax({
                        type: "POST",
                        headers: { "X-CSRFToken": csrf_token },
                        url: $(e).attr('del_url'),
                        data: {'uid':$(e).attr('data-id')},
                        dataType: 'json',
                        success: function(res){
                            if (res['status']) {
                                msg_pesan('Hapus User Sukses. ','success');
                                location.reload();
                            }else{
                                if (res['level'] == 'SISWA') {
                                    msg_pesan('Silahkan Hapus Melalui Menu Kesiswaan > Peserta Didik.', 'error')
                                }else if(res['level'] == 'GURU'){
                                    msg_pesan('Silahkan Hapus Melalui Menu Guru.', 'error')
                                }else{
                                    msg_pesan('Hapus User Gagal. ','error');
                                }
                            }
                        },
                        error: function(res){
                            msg_pesan('Hapus User Gagal. ','error');
                        }
                    });
                  }
                });
	};