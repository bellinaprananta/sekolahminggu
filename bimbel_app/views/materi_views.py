from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json, os, requests
from django.contrib import messages
from bimbel_app.models.master import (Master_user as m_user, Master_mata_pelajaran as m_mapel, Peserta_didik as m_pd, 
                                        Master_kelas as m_kelas, List_ujian as m_listujian, Master_ujian as m_ujian, Manajemen_soal as m_soal,
                                        Jawaban_soal as j_soal, Siswa_assignment as s_assignment, List_materi as m_listmateri)
from django.forms import *
from support.support_function import decrypt, encrypt, global_var, random_string_angka
from bimbel.settings import BASE_DIR, DBX_TOKEN
import re
from datetime import datetime
from django.db.models import Q
from django.template import RequestContext
import dropbox
from django.urls import reverse
from bimbel_app.views.ujian_views import Helper

class List_materiView(View):
    """docstring for List_ujianView"""
    def get(self, request):
        if global_var(request)['level'] == 'GURU':
            data_materi = m_listmateri.objects.filter(user_input = global_var(request)['uid'])
        elif global_var(request)['level'] == 'ADMIN':
            data_materi = m_listmateri.objects.all()
        else:
            data_materi = ''
        data = {
            'data_materi':data_materi,
        }
        return render(request, 'materi/list_materi.html', data)

class Create_materiView(View):
    """docstring for Create_materiView"""
    def get(self, request):
        data_kelas = m_kelas.objects.all()
        data_jenis_ujian = m_ujian.objects.all()
        data_mapel = m_mapel.objects.all()
        data_list_ujian = ''
        data_login = ''
        uuid = 0
        
        data = {
            'data_kelas':data_kelas,
            # 'type_':type_, 
            'data_list_ujian':data_list_ujian,
            'data_login':data_login,
            # 'uuid':uid,
            'data_jenis_ujian':data_jenis_ujian,
            'data_mapel':data_mapel,
            'link':reverse('bimbel_app:create_materi'),
        }
        return render(request, 'materi/create_materi.html', data)

    def post(self, request):
        judul = request.POST.get('judul')
        mapel = request.POST.get('mapel')
        jenis_broadcast = request.POST.get('group1')
        kelas = request.POST.getlist('kelas')
        file = request.FILES.getlist('filenya')
        isi_materi = request.POST.get('isi_materi')
        arr_file = []

        if jenis_broadcast != 'all':
            daftar_kelas_ =  kelas
        else:
            daftar_kelas_ = []

        for upload_file in file:
            rand_name = re.sub('[^\w\-_\. ]', '_', encrypt(str(datetime.now())))+random_string_angka()+' - '+upload_file.name.replace(' ','')

            file_path_ = os.path.join(BASE_DIR, 'bimbel_app', 'assets', 'doc_materi_temp', rand_name)
            with open(file_path_, 'wb+') as destination:
                for chunk in upload_file.chunks():
                    destination.write(chunk)

            dbx = dropbox.Dropbox(DBX_TOKEN)
            dbx.users_get_current_account()
            with open(file_path_, 'rb') as destination:
                dbx.files_upload(bytes(destination.read()), '/materi/{}'.format(rand_name))
            arr_file.append(rand_name)
            os.remove(file_path_)

        materi = m_listmateri(
                judul = judul,
                isi_materi = isi_materi,
                mata_pelajaran = m_mapel.objects.get(kode_mapel = mapel),
                kelas = jenis_broadcast,
                daftar_kelas = daftar_kelas_,
                status = 'TERBIT',
                file_support = arr_file,
                user_input = m_user.objects.get(uid=global_var(request)['uid']),
                count_see = 0,
            )
        materi.save()

        last_id_ = m_listmateri.objects.latest('id_materi')

        return redirect('bimbel_app:edit_materi', id_materi=encrypt(str(last_id_.id_materi)))

class Edit_materiView(View):
    """docstring for Create_materiView"""
    def get(self, request, id_materi):
        id_materi = decrypt(id_materi)
        data_kelas = m_kelas.objects.all()
        data_jenis_ujian = m_ujian.objects.all()
        data_mapel = m_mapel.objects.all()
        data_materi = m_listmateri.objects.get(id_materi = id_materi)
        data_list_ujian = ''
        data_login = ''
        uuid = 0
        
        data = {
            'data_kelas':data_kelas,
            'type_':'edit', 
            'data_list_ujian':data_list_ujian,
            'data_login':data_login,
            # 'uuid':uid,
            'data_jenis_ujian':data_jenis_ujian,
            'data_mapel':data_mapel,
            'data_materi':data_materi,
            'link':reverse('bimbel_app:edit_materi', args=(encrypt(id_materi),)),
        }
        return render(request, 'materi/create_materi.html', data)

    def post(self, request, id_materi):
        judul = request.POST.get('judul')
        mapel = request.POST.get('mapel')
        jenis_broadcast = request.POST.get('group1')
        kelas = request.POST.getlist('kelas')
        file = request.FILES.getlist('filenya')
        isi_materi = request.POST.get('isi_materi')
        arr_file = []

        if jenis_broadcast != 'all':
            daftar_kelas_ =  kelas
        else:
            daftar_kelas_ = []

        for upload_file in file:
            rand_name = re.sub('[^\w\-_\. ]', '_', encrypt(str(datetime.now())))+random_string_angka()+' - '+upload_file.name.replace(' ','')

            file_path_ = os.path.join(BASE_DIR, 'bimbel_app', 'assets', 'doc_materi_temp', rand_name)
            with open(file_path_, 'wb+') as destination:
                for chunk in upload_file.chunks():
                    destination.write(chunk)

            dbx = dropbox.Dropbox(DBX_TOKEN)
            dbx.users_get_current_account()
            with open(file_path_, 'rb') as destination:
                dbx.files_upload(bytes(destination.read()), '/materi/{}'.format(rand_name))
            arr_file.append(rand_name)
            os.remove(file_path_)

        materi = m_listmateri.objects.get(id_materi = decrypt(id_materi))
        materi.judul = judul
        materi.isi_materi = isi_materi
        materi.mata_pelajaran = m_mapel.objects.get(kode_mapel = mapel)
        materi.kelas = jenis_broadcast
        materi.daftar_kelas = daftar_kelas_
        
        if len(file) != 0:
            new_arr = materi.file_support
            for x in arr_file:
                new_arr.append(x)
            materi.file_support = new_arr
        materi.user_input = m_user.objects.get(uid=global_var(request)['uid'])
        materi.save()


        return redirect('bimbel_app:edit_materi', id_materi = id_materi)

class change_stat_materiView(View):
    """docstring for change_stat_materiView"""
    def post(self, request, status_):
        id_materi = decrypt(request.POST.get('xx'))
        status = False

        try:
            data_materi = m_listmateri.objects.get(id_materi = id_materi)
            data_materi.status = status_
            data_materi.save()
            status = True
        except Exception as e:
            print(e)
            status = False

        data = {
            'status':status,
        }
        return JsonResponse(data)

class del_fileView(View):
    """docstring for change_stat_materiView"""
    def post(self, request):
        id_materi = decrypt(request.POST.get('xx'))
        nama_file = request.POST.get('aa')
        status = False

        try:
            data_materi = m_listmateri.objects.get(id_materi = id_materi)
            arra_list = data_materi.file_support
            arra_list.remove(nama_file)
            data_materi.file_support = arra_list
            
            data_materi.save()

            dbx = dropbox.Dropbox(DBX_TOKEN)
            dbx.files_delete_v2('/materi/{}'.format(nama_file))
            status = True
        except Exception as e:
            print(e)
            status = False

        data = {
            'status':status,
        }
        return JsonResponse(data)

class del_materiView(View):
    """docstring for change_stat_materiView"""
    def post(self, request):
        id_materi = decrypt(request.POST.get('vv'))
        status = False

        try:
            data_materi = m_listmateri.objects.get(id_materi = id_materi)
            if data_materi.user_input.uid == global_var(request)['uid'] or global_var(request)['level'].upper() == 'ADMIN':
                for x in data_materi.file_support:
                    try:
                        dbx = dropbox.Dropbox(DBX_TOKEN)
                        dbx.files_delete_v2('/materi/{}'.format(x))
                    except Exception as e:
                        print(e)
                        pass
                
                data_materi.delete()
            status = True
        except Exception as e:
            print(e)
            status = False

        data = {
            'status':status,
        }
        return JsonResponse(data)

class lihat_materiView(View):
    """docstring for lihat_materiView"""
    def get(self, request, id_materi):
        id_materi = decrypt(id_materi)

        data_materi = m_listmateri.objects.get(id_materi=id_materi)
        data_materi_ = m_listmateri.objects.get(id_materi=id_materi)
        data_materi_.count_see = data_materi_.count_see+1

        if Helper.is_allowed_to_open(self, request, id_materi, 'materi'):
            try:
                data_materi_.save()
            except Exception as e:
                print(e)
                pass

            data = {
                'data_materi':data_materi,
            }
            return render(request, 'materi/lihat_materi.html', data)
        else:
            if global_var(request)['level'].upper() == 'SISWA':
                messages.error(request, 'Materi Bukan Diperuntukan Untuk Kelas Anda. ')
                return redirect('bimbel_app:index')
            elif global_var(request)['level'].upper() == 'GURU':
                if data_materi.user_input.uid == global_var(request)['uid']:
                    try:
                        data_materi_.save()
                    except Exception as e:
                        print(e)
                        pass

                    data = {
                        'data_materi':data_materi,
                    }
                    return render(request, 'materi/lihat_materi.html', data)
                else:
                    messages.error(request, 'Tidak Diperkenankan Melihat. ')
                    return redirect('bimbel_app:list_materi')
        
        
        
        