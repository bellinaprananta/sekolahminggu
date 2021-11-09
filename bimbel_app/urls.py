from django.contrib import admin
from django.urls import path, include
from .views import base_views
from .views import master_views
from .views import kesiswaan_views
from .views import ujian_views
from .views import materi_views
from .views import guru_views
from .views import announce_views
# from .views import penimbangan_views
# from .views import nota_views

app_name = 'bimbel_app'
urlpatterns = [
    path('', base_views.IndexView.as_view(), name = 'index'),
    path('login/', base_views.LoginView.as_view(), name = 'login'),
    path('logout/', base_views.LogoutView.as_view(), name = 'logout'),
    path('pengaturan/aplikasi/', base_views.setting_aplikasiView.as_view(), name = 'setting_aplikasi'),
    # path('join_video_conf/', base_views.join_video_confView.as_view(), name = 'join_video_conf'),
    path('master/usermanagement/', master_views.UsermanagementView.as_view(), name = 'usermanagement'),
    path('master/usermanagement/edit/<str:uid>/', master_views.UsermanagementEditView.as_view(), name = 'usermanagementedit'),
    path('master/usermanagement/delete/<str:uid>/', master_views.UsermanagementDeleteView.as_view(), name = 'usermanagementdelete'),

    path('master/mapel/', master_views.MapelView.as_view(), name = 'mapel'),
    path('master/mapel/edit/<str:kode_mapel>/', master_views.MapelEditView.as_view(), name = 'mapeledit'),
    path('master/mapel/delete/<str:kode_mapel>/', master_views.MapelDeleteView.as_view(), name = 'mapeldelete'),

    path('master/kelas/', master_views.KelasView.as_view(), name = 'kelas'),
    path('master/kelas/edit/<str:kode_kelas>/', master_views.KelasEditView.as_view(), name = 'kelasedit'),
    path('master/kelas/delete/<str:kode_kelas>/', master_views.KelasDeleteView.as_view(), name = 'kelasdelete'),

    path('master/kategori-ujian/', master_views.kategori_ujianView.as_view(), name = 'kategori_ujian'),
    path('master/kategori_ujian/edit/<str:kode_ujian>/', master_views.kategori_ujianEditView.as_view(), name = 'kategori_ujianedit'),
    path('master/kategori_ujian/delete/<str:kode_ujian>/', master_views.kategori_ujianDeleteView.as_view(), name = 'kategori_ujiandelete'),

    path('kesiswaan/pesertadidik/', kesiswaan_views.PesertaDidikView.as_view(), name = 'pesertadidik'),
    path('kesiswaan/pesertadidik/<str:type_>/<int:uid>/', kesiswaan_views.tambah_siswaView.as_view(), name = 'tambah_siswa'),
    path('kesiswaan/profil-pesertadidik/<str:type_>/<str:uid>/', kesiswaan_views.profil_siswaView.as_view(), name = 'profil_siswa'),
    path('kesiswaan/pesertadidik/<int:uid>/', kesiswaan_views.DeleteSiswaViews.as_view(), name = 'hapus_siswa'),
    path('kesiswaan/pesertadidik/validation/access-login/vali_log/', kesiswaan_views.ValidationLoginSiswaViews.as_view(), name = 'vali_log'),

    path('pengajar/guru/', guru_views.guruView.as_view(), name = 'guru'),
    path('pengajar/guru/<str:type_>/<int:uid>/', guru_views.tambah_guruView.as_view(), name = 'tambah_guru'),

    path('pengajar/profil-guru/<str:type_>/<str:uid>/', guru_views.profil_guruView.as_view(), name = 'profil_guru'),

    path('ujian/list_ujian/', ujian_views.List_ujianView.as_view(), name = 'list_ujian'),
    path('ujian/list_ujian/add_edit/<str:type_>/<str:uid>/', ujian_views.tambah_ujianView.as_view(), name = 'tambah_ujian'),
    path('ujian/list_ujian/delete/<str:uid>/', ujian_views.DeleteListUjianViews.as_view(), name = 'list_ujiandelete'),
    path('ujian/list_ujian/manajemen_soal/<str:uid>/', ujian_views.manajemen_soal_ujianView.as_view(), name = 'manajemen_soal_ujian'),
    path('ujian/list_ujian/upload_image_soal/', ujian_views.upload_image_soalViews.as_view(), name = 'upload_image_soal'),
    path('ujian/list_ujian/get_soal/', ujian_views.get_soalViews.as_view(), name = 'get_soal'),
    path('ujian/list_ujian/assignment/<str:id_ujian>/', ujian_views.kerjakan_soalViews.as_view(), name = 'kerjakan_soal'),
    path('ujian/list_ujian/get_soal_/', ujian_views.get_soaldankunciViews.as_view(), name = 'get_soaldankunci'),
    path('ujian/list_ujian/check_jawaban/', ujian_views.check_jawabanViews.as_view(), name = 'check_jawaban'),
    path('ujian/list_ujian/force_empty/', ujian_views.force_emptyViews.as_view(), name = 'force_empty'),
    path('ujian/lihat_hasil/<str:id_ujian>/', ujian_views.Lihat_hasilViews.as_view(), name = 'lihat_hasil'),
    path('ujian/change_stat_ujian/<str:status_>/', ujian_views.change_stat_ujianView.as_view(), name = 'change_stat_ujian'),
    path('ujian/peserta_ujian/<str:id_ujian>/', ujian_views.peserta_ujianView.as_view(), name = 'peserta_ujian'),

    path('materi/list_materi/', materi_views.List_materiView.as_view(), name = 'list_materi'),
    path('materi/create_materi/', materi_views.Create_materiView.as_view(), name = 'create_materi'),
    path('materi/change_stat_materi/<str:status_>/', materi_views.change_stat_materiView.as_view(), name = 'change_stat_materi'),
    path('materi/del_materi/', materi_views.del_materiView.as_view(), name = 'del_materi'),
    path('materi/edit_materi/<str:id_materi>/', materi_views.Edit_materiView.as_view(), name = 'edit_materi'),
    path('materi/del_fileView/', materi_views.del_fileView.as_view(), name = 'del_file'),
    path('materi/lihat_materi/<str:id_materi>/', materi_views.lihat_materiView.as_view(), name = 'lihat_materi'),
    
    path('pengumuman/daftar_pengumuman/', announce_views.list_announceViews.as_view(), name = 'list_announce'),
    path('pengumuman/create_pengumuman/', announce_views.Create_pengumumanView.as_view(), name = 'create_pengumuman'),
    path('pengumuman/edit_pengumuman/<str:id_pengumuman>/', announce_views.Edit_pengumumanView.as_view(), name = 'edit_pengumuman'),
    path('pengumuman/del_fileView/', announce_views.del_file_pengumumanView.as_view(), name = 'del_file_pengumuman'),
    path('pengumuman/change_stat_pengumuman/<str:status_>/', announce_views.change_stat_pengumumanView.as_view(), name = 'change_stat_pengumuman'),
    path('pengumuman/lihat_pengumuman/<str:id_pengumuman>/', announce_views.lihat_pengumumanView.as_view(), name = 'lihat_pengumuman'),
    path('pengumuman/del_pengumuman/', announce_views.del_pengumumanView.as_view(), name = 'del_pengumuman'),
] 