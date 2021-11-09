from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json, os
from django.contrib import messages
from bimbel_app.models.master import (Master_user as m_user, Master_mata_pelajaran as m_mapel, Peserta_didik as m_pd, 
                                        Master_kelas as m_kelas, List_ujian as m_listujian, Master_ujian as m_ujian, Manajemen_soal as m_soal,
                                        Jawaban_soal as j_soal, Siswa_assignment as s_assignment, List_materi as m_listmateri)
from django.forms import *
from support.support_function import decrypt, encrypt, global_var, random_string_angka
from bimbel.settings import BASE_DIR
import re
from datetime import datetime
from django.db.models import Q
from django.template import RequestContext
# from PIL import Image

class Helper:
    """docstring for ClassName"""
    def is_still_available(self, request, id_ujian):
        status = False
        status_assign = False
        status_assign_ = False

        data_ujian = m_listujian.objects.get(id_ujian = id_ujian)
        try:
            data_assign = s_assignment.objects.get(id_ujian = id_ujian, id_pd = global_var(request)['uidpd_'])
            if data_assign.status.upper() == 'SELESAI':
                status_assign = True
            elif data_assign.status.upper() == 'PROSES':
                status_assign = False
            status_assign_ = True
        except Exception as e:
            status_assign_ = False
        
        if datetime.now() >= data_ujian.tgl_tutup_auto:
            status = False
        else:
            status = True

        return status, status_assign, status_assign_

    def get_nilai_siswa(self, request, id_ujian):
        jml_soal_tampil = m_listujian.objects.get(id_ujian = id_ujian).jml_soal_tampil
        nilai_persoal = 100/jml_soal_tampil
        jml_jawaban_benar = 0
        nilai_tot = 0
        nilainya = ''

        try:
            nilainya = s_assignment.objects.get(id_ujian = id_ujian, id_pd = global_var(request)['uidpd_'])
        except Exception as e:
            pass

        if nilainya != '':
            if nilainya.status == 'SELESAI':
                kunci_jawaban = m_soal.objects.filter(kode_ujian = id_ujian).values('id_soal', 'kunci_jawaban')
                for x in kunci_jawaban:
                    try:
                        jawaban_siswa = j_soal.objects.get(id_ujian = id_ujian, id_pd = global_var(request)['uidpd_'], id_soal = x['id_soal'])
                        print(x['kunci_jawaban'], jawaban_siswa.jawaban)
                        if x['kunci_jawaban'] == jawaban_siswa.jawaban:
                            jml_jawaban_benar+=1

                    except Exception as e:
                        pass
                nilai_tot = jml_jawaban_benar * nilai_persoal
                print(jml_jawaban_benar)
            else:
                nilai_tot = 0
        return nilai_tot

    def get_nilai_siswa_batch(self, request, id_ujian, id_pd):
        jml_soal_tampil = m_listujian.objects.get(id_ujian = id_ujian).jml_soal_tampil
        nilai_persoal = 100/jml_soal_tampil
        jml_jawaban_benar = 0
        nilai_tot = 0
        nilainya = ''

        try:
            nilainya = s_assignment.objects.get(id_ujian = id_ujian, id_pd = id_pd)
        except Exception as e:
            pass

        if nilainya != '':
            if nilainya.status == 'SELESAI':
                kunci_jawaban = m_soal.objects.filter(kode_ujian = id_ujian).values('id_soal', 'kunci_jawaban')
                for x in kunci_jawaban:
                    try:
                        jawaban_siswa = j_soal.objects.get(id_ujian = id_ujian, id_pd = id_pd, id_soal = x['id_soal'])
                        print(x['kunci_jawaban'], jawaban_siswa.jawaban)
                        if x['kunci_jawaban'] == jawaban_siswa.jawaban:
                            jml_jawaban_benar+=1

                    except Exception as e:
                        pass
                nilai_tot = jml_jawaban_benar * nilai_persoal
                print(jml_jawaban_benar)
            else:
                nilai_tot = 0
        return nilai_tot

    def get_is_passing(self, request, nilainya, id_ujian):
        is_passing = False
        print(nilainya)
        kkm = m_listujian.objects.get(id_ujian = id_ujian).kkm
        if nilainya >= kkm:
            is_passing = True
        else:
            is_passing = False
        return is_passing

    def is_allowed_to_open(self, request, id_materi, jenis):
        is_allowed = False
        
        if global_var(request)['level'].upper() == 'ADMIN':
            is_allowed = True
        elif global_var(request)['level'].upper() == 'SISWA':
            data_siswa = m_pd.objects.get(uid=global_var(request)['uidpd_'])
            if jenis == 'materi':
                data_list_materi = m_listmateri.objects.get(id_materi = id_materi)
                if data_list_materi.kelas == 'all':
                    is_allowed = True
                elif data_list_materi.kelas == 'certain':
                    if data_siswa.kelas.kode_kelas in data_list_materi.daftar_kelas:
                        is_allowed = True
                    else:
                        is_allowed = False

                elif data_list_materi.kelas == 'except':
                    if data_siswa.kelas.kode_kelas not in data_list_materi.daftar_kelas:
                        is_allowed = True
                    else:
                        is_allowed = False
            elif jenis == 'assignment':
                data_list_ujian = m_listujian.objects.get(id_ujian = id_materi)
                if data_list_ujian.kelas == 'all':
                    is_allowed = True
                elif data_list_ujian.kelas == 'certain':
                    if data_siswa.kelas.kode_kelas in data_list_ujian.daftar_kelas:
                        is_allowed = True
                    else:
                        is_allowed = False

                elif data_list_ujian.kelas == 'except':
                    if data_siswa.kelas.kode_kelas not in data_list_ujian.daftar_kelas:
                        is_allowed = True
                    else:
                        is_allowed = False

        return is_allowed

class List_ujianView(View):
    """docstring for List_ujianView"""
    def get(self, request):
        data_siswa_assign = ''

        if global_var(request)['level'] == 'SISWA':
            data_siswa = m_pd.objects.get(uid=global_var(request)['uidpd_'])
            
            data_ujian = m_listujian.objects.filter(
                                Q(kelas='all') | 
                                Q(kelas='certain', daftar_kelas__contains = [data_siswa.kelas.kode_kelas]) |
                                Q(Q(kelas='except'), ~Q(daftar_kelas__contains = [data_siswa.kelas.kode_kelas])),
                                status__in = ['TERBIT', 'TUTUP']
                                )

            try:
                data_siswa_assign = s_assignment.objects.filter(id_pd = global_var(request)['uidpd_']).values_list('id_ujian','status','nilai')
                jml_siswa_assign = data_siswa_assign.count()
            except Exception as e:
                print(e)
                pass
            
            data = {
                'data_ujian':data_ujian,
                'data_siswa_assign':data_siswa_assign,
                'jml_siswa_assign':jml_siswa_assign,
            }        
            return render(request, 'ujian/list_ujian_siswa.html', data)
        else:
            if global_var(request)['level'] == 'GURU':
                data_ujian = m_listujian.objects.filter(user_input = global_var(request)['uid'])
            else:
                data_ujian = m_listujian.objects.all()
            data = {
                'data_ujian':data_ujian,
            }
            return render(request, 'ujian/list_ujian.html', data)

class tambah_ujianView(View):
    def get(self, request, type_, uid):
        data_kelas = m_kelas.objects.all()
        data_jenis_ujian = m_ujian.objects.all()
        data_mapel = m_mapel.objects.all()
        data_list_ujian = ''
        data_login = ''
        uuid = 0

        if type_ == 'edit':
            uid = decrypt(uid)
            data_list_ujian = m_listujian.objects.filter(id_ujian=uid).values()
            uuid = uid
        data = {
            'data_kelas':data_kelas,
            'type_':type_, 
            'data_list_ujian':data_list_ujian,
            'data_login':data_login,
            'uuid':uid,
            'data_jenis_ujian':data_jenis_ujian,
            'data_mapel':data_mapel,
        }
        return render(request, 'ujian/modal/add_edit_list_ujian.html', data)

    def post(self, request, type_, uid):
        judul = request.POST.get('judul')
        kategori = request.POST.get('kategori')
        deskripsi = request.POST.get('deskripsi')
        mapel = request.POST.get('mapel')
        jenis_broadcast = request.POST.get('group1')
        kelas = request.POST.getlist('kelas')
        kkm = request.POST.get('kkm')
        durasi = request.POST.get('durasi')
        durasi_min = request.POST.get('durasi_min')
        urutan_soal = request.POST.get('urutan_soal')
        jml_soal_tampil = request.POST.get('jml_soal_tampil')
        tgl_terbit = request.POST.get('tgl_terbit')
        penilaian = request.POST.get('penilaian')
        jawaban = request.POST.get('jawaban')
        password = request.POST.get('password')
        tgl_terbit_ = datetime.strptime(tgl_terbit.split(' - ')[0], '%d/%m/%Y %H:%M')
        tgl_tutup = datetime.strptime(tgl_terbit.split(' - ')[1], '%d/%m/%Y %H:%M')

        
        if jenis_broadcast != 'all':
            daftar_kelas_ =  kelas
        else:
            daftar_kelas_ = []

        if type_ == 'add':

            data_list_ujian =  m_listujian(
                    judul = judul,
                    kategori = m_ujian.objects.get(kode_ujian = kategori),
                    mata_pelajaran = m_mapel.objects.get(kode_mapel = mapel),
                    kelas = jenis_broadcast,
                    daftar_kelas = daftar_kelas_,
                    durasi = 1 if int(durasi) <= 0 else durasi,
                    durasi_minimal = 1 if int(durasi_min) <= 0 else durasi_min,
                    urutan_soal = urutan_soal,
                    jml_soal_tampil = jml_soal_tampil,
                    tgl_terbit_auto = tgl_terbit_,
                    tgl_tutup_auto = tgl_tutup,
                    tampilkan_nilai = penilaian,
                    tampilkan_jawaban = jawaban,
                    pwd = encrypt(password),
                    user_input = m_user.objects.get(uid = global_var(request)['uid']),
                    status = 'KONSEP',
                    deskripsi = deskripsi,
                    kkm = kkm,
                    )
            data_list_ujian.save()
            messages.success(request, 'Tambah Ujian Sukses !')

        elif type_ == 'edit':
            uid = decrypt(uid)
            data_list_ujian = m_listujian.objects.get(id_ujian=uid)
            
            if data_list_ujian.status.upper() == 'KONSEP' or data_list_ujian.status.upper() == 'TERBIT':
                data_list_ujian.judul = judul
                data_list_ujian.kategori = m_ujian.objects.get(kode_ujian = kategori)
                data_list_ujian.mata_pelajaran = m_mapel.objects.get(kode_mapel = mapel)
                data_list_ujian.kelas = jenis_broadcast
                data_list_ujian.daftar_kelas = daftar_kelas_
                data_list_ujian.durasi = 1 if int(durasi) <= 0 else durasi
                data_list_ujian.durasi_minimal = 1 if int(durasi_min) <= 0 else durasi_min
                data_list_ujian.urutan_soal = urutan_soal
                data_list_ujian.jml_soal_tampil = jml_soal_tampil
                data_list_ujian.tgl_terbit_auto = tgl_terbit_
                data_list_ujian.tgl_tutup_auto = tgl_tutup
                data_list_ujian.tampilkan_nilai = penilaian
                data_list_ujian.tampilkan_jawaban = jawaban
                data_list_ujian.pwd = encrypt(password)
                data_list_ujian.user_input = m_user.objects.get(uid = global_var(request)['uid'])
                data_list_ujian.deskripsi = deskripsi
                data_list_ujian.kkm = kkm

                data_list_ujian.save()
                messages.success(request, 'Edit Ujian Sukses !')
        else:
            messages.error(request, 'Method Not Allowed !')
        data = {}

        return redirect('bimbel_app:list_ujian')

class DeleteListUjianViews(View):
    """docstring for DeleteBarang"""
    def post(self, request, uid):
        uid = decrypt(uid)
        status = False
        protected = False
        data_list_ujian = m_listujian.objects.get(id_ujian=uid)

        try:
            if data_list_ujian.status.upper() == 'KONSEP' or data_list_ujian.status.upper() == 'TERBIT':
                if global_var(request)['level'].upper() == 'GURU':
                    if data_list_ujian.user_input.uid == global_var(request)['uid']:
                        data_list_ujian.delete()
                elif global_var(request)['level'].upper() == 'ADMIN':
                    data_list_ujian.delete()

                status = True
            else:
                protected = True
                status = False
        except Exception as e:
            print(e)
            status = False

        data = {
            'status':status,
            'protected':protected,
        }
        return JsonResponse(data)

class manajemen_soal_ujianView(View):
    """docstring for manajemen_soal_ujianView"""
    def get(self, request, uid):
        uid = decrypt(uid)
        arr_data = []

        data_ujian = m_listujian.objects.get(id_ujian=uid)
        if data_ujian.status.upper() == 'KONSEP':
            data_soal = m_soal.objects.filter(kode_ujian=uid)
            for xx in data_soal:
                arr_data.append(xx.no_soal)

            data = {
                'data_ujian':data_ujian,
                'data_soal':data_soal,
                'jml_soal':data_soal.count(),
                'arr_data':arr_data,
            }
            return render(request, 'ujian/manajemen_soal.html', data)
        else:
            if data_ujian.status.upper() == 'TERBIT':
                messages.error(request, 'Tidak Bisa Mengubah Soal, Ujian Sudah Diterbitkan. ')
            elif data_ujian.status.upper() == 'TUTUP':
                messages.error(request, 'Tidak Bisa Mengubah Soal, Ujian Sudah Ditutup. ')
            return redirect('bimbel_app:list_ujian')

    def post(self, request, uid):
        uid = decrypt(uid)
        kode_ujian = m_listujian.objects.get(id_ujian=uid)
        uraian_soal = request.POST.get('soal')
        jawaban1 = request.POST.get('jawaban1')
        jawaban2 = request.POST.get('jawaban2')
        jawaban3 = request.POST.get('jawaban3')
        jawaban4 = request.POST.get('jawaban4')
        jawaban5 = request.POST.get('jawaban5')
        kunci_jawaban = request.POST.get('kunci_jawaban')
        soalke = request.POST.get('soalke')

        data_soal_ = m_soal.objects.filter(kode_ujian = uid, no_soal = soalke)
        if data_soal_.count() == 0:
            data_soal = m_soal(
                kode_ujian = m_listujian.objects.get(id_ujian=uid),
                no_soal = soalke, 
                uraian_soal = uraian_soal, 
                jawaban1 = jawaban1,
                jawaban2 = jawaban2,
                jawaban3 = jawaban3,
                jawaban4 = jawaban4,
                jawaban5 = jawaban5,
                kunci_jawaban = kunci_jawaban,
                user_input = m_user.objects.get(uid=global_var(request)['uid'])
                )
            try:
                if kunci_jawaban:
                    data_soal.save()
                    messages.success(request, 'Simpan Soal No - {} Sukses.'.format(soalke))
                else:
                    messages.error(request, 'Kunci Jawaban Harus Dipilih. ')
            except Exception as e:
                print(e)
                messages.error(request, 'Simpan Soal No - {} Gagal.'.format(soalke))
        else:
            data_soal_ = m_soal.objects.get(kode_ujian = uid, no_soal = soalke)

            data_soal_.uraian_soal = uraian_soal
            data_soal_.jawaban1 = jawaban1
            data_soal_.jawaban2 = jawaban2
            data_soal_.jawaban3 = jawaban3
            data_soal_.jawaban4 = jawaban4
            data_soal_.jawaban5 = jawaban5
            data_soal_.kunci_jawaban = kunci_jawaban
            data_soal_.user_input = m_user.objects.get(uid=global_var(request)['uid'])

            try:
                if kunci_jawaban:
                    data_soal_.save()
                    messages.success(request, 'Edit Soal No - {} Sukses.'.format(soalke))
                else:
                    messages.error(request, 'Kunci Jawaban Harus Dipilih. ')
            except Exception as e:
                print(e)
                messages.error(request, 'Edit Soal No - {} Gagal.'.format(soalke))
            
        return redirect('bimbel_app:manajemen_soal_ujian', uid=encrypt(str(uid)))

class upload_image_soalViews(View):
    """docstring for manajemen_soal_ujianView"""
    def post(self, request):
        
        data = {
            
        }
        return JsonResponse(data)

class get_soalViews(View):
    """docstring for manajemen_soal_ujianView"""
    def post(self, request):
        status = False
        data_soal = ''
        kode_ujian = decrypt(request.POST.get('kode_ujian'))
        no_soal = request.POST.get('no_soal')

        
        try:
            data_soal = m_soal.objects.filter(kode_ujian = kode_ujian, no_soal=no_soal).values()
            status = True
        except Exception as e:
            print(e)
            status = False

        data = {
            'status':status, 
            'data_soal':list(data_soal),         
        }
        return JsonResponse(data)

class get_soaldankunciViews(View):
    """docstring for manajemen_soal_ujianView"""
    def post(self, request):
        status = False
        data_soal = ''
        data_jawaban_soalnya = ''
        kode_ujian = decrypt(request.POST.get('kode_ujian'))
        no_soal = request.POST.get('no_soal')
        kode_soal = request.POST.get('kode_soal')
        
        try:
            data_soal = m_soal.objects.filter(kode_ujian = kode_ujian, no_soal=no_soal).values('id_soal', 'uraian_soal', 'jawaban1', 'jawaban2', 'jawaban3', 'jawaban4', 'jawaban5')
            data_jawaban_soalnya = j_soal.objects.filter(id_ujian = kode_ujian, id_soal=data_soal[0]['id_soal'], id_pd = global_var(request)['uidpd_']).values('jawaban')
            status = True
        except Exception as e:
            print(e)
            status = False

        data = {
            'status':status, 
            'data_soal':list(data_soal),
            'data_jawaban_soalnya':list(data_jawaban_soalnya),    
        }
        return JsonResponse(data)
        

class kerjakan_soalViews(View):
    """docstring for kerjakan_soal"""
    def get(self, request, id_ujian):
        uid = decrypt(id_ujian)
        arr_data = []

        data_ujian = m_listujian.objects.get(id_ujian=uid)
        
        if Helper.is_allowed_to_open(self, request, uid, 'assignment'):
            if data_ujian.status.upper() == 'TERBIT':
                if Helper().is_still_available(request, uid)[0]:
                    is_assign = s_assignment.objects.filter(id_ujian = uid, id_pd = global_var(request)['uidpd_'])
                    
                    if is_assign.count() == 0:
                        input_assign = s_assignment(id_ujian = m_listujian.objects.get(id_ujian = uid),
                                        id_pd = m_pd.objects.get(uid = global_var(request)['uidpd_']),
                                        user_input = m_user.objects.get(uid = global_var(request)['uid']),
                                        status = 'PROSES')
                        input_assign.save()

                    if is_assign.count() == 1:
                        
                            if not Helper().is_still_available(request, uid)[1]: 
                                data_soal = m_soal.objects.filter(kode_ujian=uid)

                                for xx in data_soal:
                                    arr_data.append(xx.no_soal)

                                data = {
                                    'data_ujian':data_ujian,
                                    'data_soal':data_soal,
                                    'jml_soal':data_soal.count(),
                                    'arr_data':arr_data,
                                }
                                return render(request, 'ujian/assignment.html', data)
                            else:
                                messages.error(request, 'Ujian Telah Selesai Anda Kerjakan. ')
                                return redirect('bimbel_app:list_ujian')
                    else:
                        messages.error(request, 'Error Retrieving Data, Please Contact Administrator. ')
                        return redirect('bimbel_app:list_ujian')
                elif Helper().is_still_available(request, uid)[1]:
                    messages.error(request, 'Ujian Telah Selesai Anda Kerjakan. ')
                    return redirect('bimbel_app:list_ujian')
                else:
                    messages.error(request, 'Sesi Ujian Sudah Berakhir. ')
                    return redirect('bimbel_app:list_ujian')
            else:
                if data_ujian.status.upper() == 'KONSEP':
                    messages.error(request, 'Tidak Bisa Mengerjakan Soal, Ujian Belum Diterbitkan. ')
                elif data_ujian.status.upper() == 'TUTUP':
                    messages.error(request, 'Tidak Bisa Mengubah Soal, Ujian Sudah Ditutup. ')
                return redirect('bimbel_app:list_ujian')
        else:
            messages.error(request, 'Ujian Bukan Diperuntukan Untuk Kelas Anda.')
            return redirect('bimbel_app:list_ujian')

    def post(self, request, id_ujian):
        uid = decrypt(id_ujian)
        status = False
        if Helper().is_still_available(request, uid)[0]:
            id_soal = request.POST.get('id_soal')
            jawaban = request.POST.get('jawaban')
            jawaban_soalnya = j_soal(
                            id_ujian = m_listujian.objects.get(id_ujian=uid),
                            id_soal = m_soal.objects.get(id_soal=id_soal),
                            jawaban = jawaban,
                            id_pd = m_pd.objects.get(uid=global_var(request)['uidpd_']),
                            user_input = m_user.objects.get(uid=global_var(request)['uid']),

                            )
            try:
                jawaban_soalnya.save(force_insert=True)
                status = True
            except Exception as e:
                try:
                    data_j = j_soal.objects.filter(id_ujian = uid, id_soal = id_soal, id_pd = global_var(request)['uidpd_']).update(jawaban = jawaban, id_pd = m_pd.objects.get(uid=global_var(request)['uidpd_']), 
                            user_input = m_user.objects.get(uid=global_var(request)['uid']),
                            tgl_input=datetime.now(),
                            updated_at=datetime.now())

                    status = True
                except Exception as e:
                    print(e)
                    status = False           
        data = {
            'status':status,
            'is_still_available':Helper().is_still_available(request, uid)[0],
            'is_finished':Helper().is_still_available(request, uid)[1],
        }
        return JsonResponse(data)

class check_jawabanViews(View):
    def post(self, request):
        id_ujian = decrypt(request.POST.get('id_ujian'))
        id_soal = request.POST.get('id_soal')
        is_complete = False
        is_finish = False
        is_empty_possibility = False
        jml_jawaban_kosong = 0

        check_jawaban = j_soal.objects.filter(id_ujian = id_ujian, id_pd = global_var(request)['uidpd_'])
        val_check_jawaban = check_jawaban.values()
        jml_check_jawaban = check_jawaban.count()
        jml_soal_ujian = m_listujian.objects.get(id_ujian = id_ujian).jml_soal_tampil
        
        if jml_soal_ujian == jml_check_jawaban:
            is_complete = True
        if is_complete:
            s_assignment_ = s_assignment.objects.get(id_ujian = id_ujian, id_pd = global_var(request)['uidpd_'])
            s_assignment_.status = 'SELESAI'
            s_assignment_.save()
            is_finish = True

        for x in val_check_jawaban:
            if x['jawaban'] == '':
                jml_jawaban_kosong+=1

        if jml_jawaban_kosong != 0:
            is_empty_possibility = True

        data = {
            'is_complete':is_complete,
            'jml_jawaban_kosong':jml_jawaban_kosong,
            'is_empty_possibility':is_empty_possibility,
            'is_finish':is_finish,
        }
        return JsonResponse(data)

class force_emptyViews(View):
    def post(self, request):
        id_ujian = decrypt(request.POST.get('id_ujian'))
        id_soal = request.POST.get('id_soal')
        status = False
        list_j_soal = []

        check_jawaban = j_soal.objects.filter(id_ujian = id_ujian, id_pd = global_var(request)['uidpd_'])
        val_check_jawaban = check_jawaban.values('id_soal')
        jml_soal_ujian = m_listujian.objects.get(id_ujian = id_ujian).jml_soal_tampil
        detail_soal = m_soal.objects.filter(kode_ujian = id_ujian).values('id_soal','no_soal')
        
        try:
            for xx in val_check_jawaban:
                list_j_soal.append(xx['id_soal'])
            
            for x in detail_soal:
                if x['id_soal'] not in list_j_soal:
                    
                    jsoal = j_soal(
                            id_ujian = m_listujian.objects.get(id_ujian=id_ujian),
                            id_soal = m_soal.objects.get(id_soal=x['id_soal']),
                            jawaban = '',
                            id_pd = m_pd.objects.get(uid=global_var(request)['uidpd_']),
                            user_input = m_user.objects.get(uid=global_var(request)['uid']),

                            )
                    jsoal.save(force_insert=True)         

                s_assignment_ = s_assignment.objects.get(id_ujian = id_ujian, id_pd = global_var(request)['uidpd_'])
                s_assignment_.status = 'SELESAI'
                s_assignment_.save()

            status = True
        except Exception as e:
            print(e)
            status = False

        data = {
            'status':status,
        }
        return JsonResponse(data)

class Lihat_hasilViews(View):
    """docstring for Detail"""
    def get(self, request, id_ujian):
        uid = decrypt(id_ujian)
        arr_data = []

        data_ujian = m_listujian.objects.get(id_ujian=uid)

        if data_ujian.status.upper() == 'TERBIT':
            
            if not Helper().is_still_available(request, uid)[0] or Helper().is_still_available(request, uid)[1]:
                is_assign = s_assignment.objects.filter(id_ujian = uid, id_pd = global_var(request)['uidpd_'])
                
                if is_assign.count() == 0:
                    input_assign = s_assignment(id_ujian = m_listujian.objects.get(id_ujian = uid),
                                    id_pd = m_pd.objects.get(uid = global_var(request)['uidpd_']),
                                    user_input = m_user.objects.get(uid = global_var(request)['uid']),
                                    status = 'PROSES')
                    input_assign.save()

                if is_assign.count() == 1:
                    
                        data_soal = m_soal.objects.filter(kode_ujian=uid)

                        for xx in data_soal:
                            arr_data.append(xx.no_soal)

                        data = {
                            'data_ujian':data_ujian,
                            'data_soal':data_soal,
                            'jml_soal':data_soal.count(),
                            'arr_data':arr_data,
                        }
                        return render(request, 'ujian/lihat_hasil.html', data)
                else:
                    messages.error(request, 'Error Retrieving Data, Please Contact Administrator. ')
                    return redirect('bimbel_app:list_ujian')
            elif not Helper().is_still_available(request, uid)[1]:
                messages.error(request, 'Ujian Belum Selesai Anda Kerjakan. ')
                return redirect('bimbel_app:list_ujian')
            else:
                messages.error(request, 'Sesi Ujian Sudah Berakhir. ')
                return redirect('bimbel_app:list_ujian')
        else:
            if data_ujian.status.upper() == 'KONSEP':
                messages.error(request, 'Tidak Bisa Mengerjakan Soal, Ujian Belum Diterbitkan. ')
            elif data_ujian.status.upper() == 'TUTUP':
                messages.error(request, 'Tidak Bisa Mengubah Soal, Ujian Sudah Ditutup. ')
            return redirect('bimbel_app:list_ujian')

    def post(self, request, id_ujian):
        status = False
        data_soal = ''
        data_jawaban_soalnya = ''
        kode_ujian = decrypt(id_ujian)
        no_soal = request.POST.get('no_soal')
        
        try:
            data_soal = m_soal.objects.filter(kode_ujian = kode_ujian, no_soal=no_soal).values('id_soal', 'uraian_soal', 'jawaban1', 'jawaban2', 'jawaban3', 'jawaban4', 'jawaban5', 'kunci_jawaban')
            data_jawaban_soalnya = j_soal.objects.filter(id_ujian = kode_ujian, id_soal=data_soal[0]['id_soal'], id_pd = global_var(request)['uidpd_']).values('jawaban')
            status = True
        except Exception as e:
            print(e)
            status = False

        data = {
            'status':status, 
            'data_soal':list(data_soal),
            'data_jawaban_soalnya':list(data_jawaban_soalnya),    
        }
        return JsonResponse(data)

class change_stat_ujianView(View):
    """docstring for change_stat_ujianView"""
    def post(self, request, status_):
        id_ujian = decrypt(request.POST.get('xx'))
        status = False

        try:
            data_ujian = m_listujian.objects.get(id_ujian = id_ujian)
            data_ujian.status = status_
            data_ujian.save()
            status = True
        except Exception as e:
            print(e)
            status = False

        data = {
            'status':status,
        }
        return JsonResponse(data)

class peserta_ujianView(View):
    """docstring for peserta_ujianView"""
    def get(self, request, id_ujian):
        id_ujian = decrypt(id_ujian)

        list_peserta = s_assignment.objects.filter(id_ujian = id_ujian)
        print(list_peserta)
        data = {
            'list_peserta':list_peserta,
        }
        return render(request, 'ujian/peserta_ujian.html', data)
        
        

        
        
        
        
        
