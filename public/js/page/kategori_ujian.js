$(document).ready(function(){
		$('#table_user').DataTable( {
		dom: 'Bfrtip',
		buttons: [
			'excel', 'pdf'
		]
	} );

		
	})

	function edit_ujian(e){
		$.ajax({
            type: "GET",
            // headers: { "X-CSRFToken": csrf_token },
            url: $(e).attr('edit_url'),
            data: {'kode_ujian':$(e).attr('data-id')},
            dataType: 'json',
            success: function(res){
            	data = res['data_ujian'][0];
            	$('#id_nama_ujian').val(data['nama_ujian']);
            	$('#id_kode_ujian').val('s');
            	$('#kode_ujian_div').css('display', 'none');
            	$('#cancel_edit').css('display', '');
            	$('#frm_ujian').attr('action', $(e).attr('edit_url'))
            },
            error: function(res){
                msg_pesan('Hapus Item Gagal. ','error');
                $('#frm_ujian').attr('action', "{% url 'bimbel_app:kategori_ujian' %}");
                $('#cancel_edit').css('display', 'none');
            }
        });
	};

	function delete_ujian(e){
		Swal.fire({
              title: 'Yakin mau menghapus Ujian \"'+$(e).attr('data-u')+'\" ?',
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
                            msg_pesan('Hapus Ujian Sukses. ','success');
                            location.reload();
                        }else{
                            if (res['is_affiliate']) {
                                msg_pesan('Hapus Ujian Gagal. Ujian Sudah Dipakai. ','error');
                            }else{
                                msg_pesan('Hapus Ujian Gagal. ','error');
                            }
                        }
                    },
                    error: function(res){
                        msg_pesan('Hapus Ujian Gagal. ','error');
                    }
                });
              }
            });
	};