$(document).ready(function(){
		$('#table_user').DataTable( {
		dom: 'Bfrtip',
		buttons: [
			'excel', 'pdf'
		]
	} );

		
	})

	function edit_mapel(e){
		$.ajax({
            type: "GET",
            // headers: { "X-CSRFToken": csrf_token },
            url: $(e).attr('edit_url'),
            data: {'kode_mapel':$(e).attr('data-id')},
            dataType: 'json',
            success: function(res){
            	data = res['data_mapel'][0];
            	$('#id_nama_mapel').val(data['nama_mapel']);
            	$('#id_kode_mapel').val('s');
            	$('#kode_mapel_div').css('display', 'none');
            	$('#cancel_edit').css('display', '');
            	$('#frm_mapel').attr('action', $(e).attr('edit_url'))
            },
            error: function(res){
                msg_pesan('Hapus Item Gagal. ','error');
                $('#frm_mapel').attr('action', "{% url 'bimbel_app:mapel' %}");
                $('#cancel_edit').css('display', 'none');
            }
        });
	};

	function delete_mapel(e){
		Swal.fire({
              title: 'Yakin mau menghapus Mata Pelajaran \"'+$(e).attr('data-u')+'\" ?',
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
                            msg_pesan('Hapus Mata Pelajaran Sukses. ','success');
                            location.reload();
                        }else{
                            if (res['is_affiliate']) {
                                msg_pesan('Hapus Mata Pelajaran Gagal. Mata Pelajaran Sudah Dipakai. ','error');
                            }else{
                                msg_pesan('Hapus Mata Pelajaran Gagal. ','error');
                            }
                        }
                    },
                    error: function(res){
                        msg_pesan('Hapus Mata Pelajaran Gagal. ','error');
                    }
                });
              }
            });
	};