from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

class Master_user(models.Model):
    uid = models.AutoField(blank=False, null=False, primary_key=True)
    uname = models.TextField(blank=False, null=False)
    pwd = models.TextField(blank=False, null=False)
    fullname = models.TextField(blank=False, null=False)
    nip = models.TextField(blank=False, null=False)
    level = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'master\".\"master_user'
        ordering = ['uname']

class Master_mata_pelajaran(models.Model):
    kode_mapel = models.TextField(blank=False, null=False, primary_key=True)
    nama_mapel = models.TextField(blank=False, null=False)
    user_input = models.ForeignKey(Master_user, on_delete=models.PROTECT, db_column='user_input')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'master\".\"master_mata_pelajaran'
        ordering = ['kode_mapel']

class Master_kelas(models.Model):
    kode_kelas = models.TextField(blank=False, null=False, primary_key=True)
    nama_kelas = models.TextField(blank=False, null=False)
    user_input = models.ForeignKey(Master_user, on_delete=models.PROTECT, db_column='user_input')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'master\".\"master_kelas'
        ordering = ['kode_kelas']

class Master_ujian(models.Model):
    kode_ujian = models.TextField(blank=False, null=False, primary_key=True)
    nama_ujian = models.TextField(blank=False, null=False)
    user_input = models.ForeignKey(Master_user, on_delete=models.PROTECT, db_column='user_input')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'master\".\"master_ujian'
        ordering = ['kode_ujian']


class Peserta_didik(models.Model):
    uid = models.AutoField(blank=False, null=False, primary_key=True)
    nama_siswa = models.TextField(blank=False, null=False)
    nis = models.TextField(blank=False, null=False)
    kelas = models.ForeignKey(Master_kelas, on_delete=models.PROTECT, db_column='kelas')
    jenis_kelamin = models.CharField(blank=False, null=False, max_length = 1)
    tempat_lahir = models.TextField(blank=False, null=False)
    tanggal_lahir = models.DateField()
    alamat = models.TextField(blank=False, null=False)
    agama = models.TextField(blank=False, null=False)
    no_hp = models.TextField(blank=False, null=False)
    tahun_registrasi = models.CharField(blank=False, null=False, max_length = 4)
    status = models.CharField(blank=False, null=False, max_length = 1)
    informasi_lain = models.TextField(blank=False, null=False)
    foto = models.TextField(blank=False, null=False)
    email = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_input = models.ForeignKey(Master_user, on_delete=models.PROTECT, db_column='user_input')

    class Meta:
        managed = False
        db_table = 'kesiswaan\".\"peserta_didik'
        ordering = ['uid']

class Master_guru(models.Model):
    uid = models.AutoField(blank=False, null=False, primary_key=True)
    nama_guru = models.TextField(blank=False, null=False)
    nip = models.TextField(blank=False, null=False)
    jenis_kelamin = models.CharField(blank=False, null=False, max_length = 1)
    tempat_lahir = models.TextField(blank=False, null=False)
    tanggal_lahir = models.DateField()
    alamat = models.TextField(blank=False, null=False)
    agama = models.TextField(blank=False, null=False)
    no_hp = models.TextField(blank=False, null=False)
    tahun_registrasi = models.CharField(blank=False, null=False, max_length = 4)
    status = models.CharField(blank=False, null=False, max_length = 1)
    informasi_lain = models.TextField(blank=False, null=False)
    foto = models.TextField(blank=False, null=False)
    email = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_input = models.ForeignKey(Master_user, on_delete=models.PROTECT, db_column='user_input')

    class Meta:
        managed = False
        db_table = 'kesiswaan\".\"guru'
        ordering = ['uid']

class List_ujian(models.Model):
    id_ujian = models.AutoField(blank=False, null=False, primary_key=True)
    judul = models.TextField(blank=False, null=False)
    kategori = models.ForeignKey(Master_ujian, on_delete=models.PROTECT, db_column='kategori')
    mata_pelajaran = models.ForeignKey(Master_mata_pelajaran, on_delete=models.PROTECT, db_column='mata_pelajaran')
    kelas = models.CharField(blank=False, null=False, max_length = 1)
    daftar_kelas = ArrayField(models.CharField(max_length=200),size=1)
    durasi = models.IntegerField(blank=False, null=False)
    durasi_minimal = models.IntegerField(blank=False, null=False)
    urutan_soal = models.CharField(blank=False, null=False, max_length = 1)
    jml_soal_tampil = models.IntegerField(blank=False, null=False)
    tgl_terbit_auto = models.DateTimeField()
    tgl_tutup_auto = models.DateTimeField()
    tampilkan_nilai = models.TextField(blank=False, null=False)
    tampilkan_jawaban = models.TextField(blank=False, null=False)
    pwd = models.TextField(blank=False, null=False)
    user_input = models.ForeignKey(Master_user, on_delete=models.PROTECT, db_column='user_input')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.TextField(blank=False, null=False)
    deskripsi = models.TextField(blank=False, null=False)
    kkm = models.FloatField(blank=False, null=False)

    class Meta:
        managed = False
        db_table = 'ujian\".\"list_ujian'
        ordering = ['id_ujian']

class Manajemen_soal(models.Model):
    id_soal = models.AutoField(blank=False, null=False, primary_key=True)
    kode_ujian = models.ForeignKey(List_ujian, on_delete=models.PROTECT, db_column='kode_ujian')
    no_soal = models.IntegerField(blank=False, null=False)
    uraian_soal = models.TextField(blank=False, null=False)
    jawaban1 = models.TextField(blank=False, null=False)
    jawaban2 = models.TextField(blank=False, null=False)
    jawaban3 = models.TextField(blank=False, null=False)
    jawaban4 = models.TextField(blank=False, null=False)
    jawaban5 = models.TextField(blank=False, null=False)
    kunci_jawaban = models.CharField(blank=False, null=False, max_length = 1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_input = models.ForeignKey(Master_user, on_delete=models.PROTECT, db_column='user_input')

    class Meta:
        managed = False
        db_table = 'ujian\".\"manajemen_soal'
        ordering = ['id_soal']

class Jawaban_soal(models.Model):
    id_ujian = models.OneToOneField(List_ujian, on_delete=models.PROTECT, db_column='id_ujian', unique=True,  primary_key=True)
    id_soal = models.OneToOneField(Manajemen_soal, on_delete=models.PROTECT, db_column='id_soal', unique = True)
    jawaban = models.CharField(blank=False, null=False, max_length = 1)
    id_pd = models.OneToOneField(Peserta_didik, on_delete=models.PROTECT, db_column='id_pd', unique = True)
    tgl_input = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_input = models.ForeignKey(Master_user, on_delete=models.PROTECT, db_column='user_input')

    class Meta:
        managed = False
        db_table = 'ujian\".\"jawaban_soal'
        ordering = ['id_ujian']

class Siswa_assignment(models.Model):
    id_siswa_assignment = models.AutoField(blank=False, null=False, primary_key=True)
    id_ujian = models.ForeignKey(List_ujian, on_delete=models.PROTECT, db_column='id_ujian')
    id_pd = models.ForeignKey(Peserta_didik, on_delete=models.PROTECT, db_column='id_pd')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_input = models.ForeignKey(Master_user, on_delete=models.PROTECT, db_column='user_input')
    status = models.TextField(blank=False, null=False)
    nilai = models.DecimalField(blank=False, null=False, decimal_places = 2, max_digits = 4)

    class Meta:
        managed = False
        db_table = 'ujian\".\"siswa_assignment'
        ordering = ['id_siswa_assignment']


class List_materi(models.Model):
    id_materi = models.AutoField(blank=False, null=False, primary_key=True)
    judul = models.TextField(blank=False, null=False)
    isi_materi = models.TextField(blank=False, null=False)
    mata_pelajaran = models.ForeignKey(Master_mata_pelajaran, on_delete=models.PROTECT, db_column='mata_pelajaran')
    kelas = models.TextField(blank=False, null=False)
    daftar_kelas = ArrayField(models.TextField(max_length=200),size=1)
    status = models.TextField(blank=False, null=False)
    file_support = ArrayField(models.TextField(max_length=1000),size=1)
    user_input = models.ForeignKey(Master_user, on_delete=models.PROTECT, db_column='user_input')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    count_see = models.IntegerField(blank=False, null=False)

    class Meta:
        managed = False
        db_table = 'materi\".\"list_materi'
        ordering = ['id_materi']

class List_pengumuman(models.Model):
    id_pengumuman = models.AutoField(blank=False, null=False, primary_key=True)
    judul = models.TextField(blank=False, null=False)
    isi_materi = models.TextField(blank=False, null=False)
    tgl_terbit_auto = models.DateTimeField()
    tgl_tutup_auto = models.DateTimeField()
    status = models.TextField(blank=False, null=False)
    file_support = ArrayField(models.TextField(max_length=1000),size=1)
    user_input = models.ForeignKey(Master_user, on_delete=models.PROTECT, db_column='user_input')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    count_see = models.IntegerField(blank=False, null=False)

    class Meta:
        managed = False
        db_table = 'announce\".\"daftar_pengumuman'
        ordering = ['id_pengumuman']


class Master_aplikasi(models.Model):
    jenis = models.TextField(blank=False, null=False, primary_key=True)
    nama = models.TextField(blank=False, null=False)
    alamat = models.TextField(blank=False, null=False)
    no_hp = models.TextField(blank=False, null=False)
    foto = models.TextField(blank=False, null=False)
    email = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_input = models.ForeignKey(Master_user, on_delete=models.PROTECT, db_column='user_input')

    class Meta:
        managed = False
        db_table = 'master\".\"aplikasi'
        ordering = ['jenis']


        
        

        
