$(document).ready(function(){
		$('#table_user').DataTable( {
		dom: 'Bfrtip',
		buttons: [
			'excel', 'pdf'
		]
	} );

		
	})

	function edit_kelas(e){
		$.ajax({
            type: "GET",
            // headers: { "X-CSRFToken": csrf_token },
            url: $(e).attr('edit_url'),
            data: {'kode_kelas':$(e).attr('data-id')},
            dataType: 'json',
            success: function(res){
            	data = res['data_kelas'][0];
            	$('#id_nama_kelas').val(data['nama_kelas']);
            	$('#id_kode_kelas').val('s');
            	$('#kode_kelas_div').css('display', 'none');
            	$('#cancel_edit').css('display', '');
            	$('#frm_kelas').attr('action', $(e).attr('edit_url'))
            },
            error: function(res){
                msg_pesan('Hapus Item Gagal. ','error');
                $('#frm_kelas').attr('action', "{% url 'bimbel_app:kelas' %}");
                $('#cancel_edit').css('display', 'none');
            }
        });
	};

	function delete_kelas(e){
		Swal.fire({
              title: 'Yakin mau menghapus Kelas \"'+$(e).attr('data-u')+'\" ?',
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
                            msg_pesan('Hapus Kelas Sukses. ','success');
                            location.reload();
                        }else{
                            if (res['is_affiliate']) {
                                msg_pesan('Hapus Kelas Gagal. Kelas Sudah Dipakai. ','error');
                            }else{
                                msg_pesan('Hapus Kelas Gagal. ','error');
                            }
                        }
                    },
                    error: function(res){
                        msg_pesan('Hapus Kelas Gagal. ','error');
                    }
                });
              }
            });
	};