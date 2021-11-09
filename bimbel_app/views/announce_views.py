from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json, os, requests
from django.contrib import messages
from bimbel_app.models.master import (Master_user as m_user, Master_mata_pelajaran as m_mapel, Peserta_didik as m_pd, 
                                        Master_kelas as m_kelas, List_ujian as m_listujian, Master_ujian as m_ujian, Manajemen_soal as m_soal,
                                        Jawaban_soal as j_soal, Siswa_assignment as s_assignment, List_materi as m_listmateri,
                                        List_pengumuman as m_listpengumuman)
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

class list_announceViews(View):
    """docstring for List_ujianView"""
    def get(self, request):
        if global_var(request)['level'] == 'GURU':
            data_pengumuman = m_listpengumuman.objects.filter(user_input = global_var(request)['uid'])
        elif global_var(request)['level'] == 'ADMIN':
            data_pengumuman = m_listpengumuman.objects.all()
        else:
            data_pengumuman = ''
        data = {
            'data_pengumuman':data_pengumuman,
        }
        return render(request, 'announce/list_pengumuman.html', data)

class Create_pengumumanView(View):
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
            'link':reverse('bimbel_app:create_pengumuman'),
        }
        return render(request, 'announce/create_pengumuman.html', data)

    def post(self, request):
        judul = request.POST.get('judul')
        tgl_terbit = request.POST.get('tgl_terbit')
        file = request.FILES.getlist('filenya')
        isi_materi = request.POST.get('isi_materi')
        arr_file = []

        tgl_terbit_ = datetime.strptime(tgl_terbit.split(' - ')[0], '%d/%m/%Y %H:%M')
        tgl_tutup = datetime.strptime(tgl_terbit.split(' - ')[1], '%d/%m/%Y %H:%M')


        for upload_file in file:
            rand_name = re.sub('[^\w\-_\. ]', '_', encrypt(str(datetime.now())))+random_string_angka()+' - '+upload_file.name.replace(' ','')

            file_path_ = os.path.join(BASE_DIR, 'bimbel_app', 'assets', 'doc_materi_temp', rand_name)
            with open(file_path_, 'wb+') as destination:
                for chunk in upload_file.chunks():
                    destination.write(chunk)

            dbx = dropbox.Dropbox(DBX_TOKEN)
            dbx.users_get_current_account()
            with open(file_path_, 'rb') as destination:
                dbx.files_upload(bytes(destination.read()), '/pengumuman/{}'.format(rand_name))
            arr_file.append(rand_name)
            os.remove(file_path_)

        pengumuman = m_listpengumuman(
                judul = judul,
                isi_materi = isi_materi,
                status = 'TERBIT',
                tgl_terbit_auto = tgl_terbit_,
                tgl_tutup_auto = tgl_tutup,
                file_support = arr_file,
                user_input = m_user.objects.get(uid=global_var(request)['uid']),
                count_see = 0,
            )
        pengumuman.save()

        last_id_ = m_listpengumuman.objects.latest('id_pengumuman')

        return redirect('bimbel_app:edit_pengumuman', id_pengumuman=encrypt(str(last_id_.id_pengumuman)))

class Edit_pengumumanView(View):
    """docstring for Create_materiView"""
    def get(self, request, id_pengumuman):
        id_pengumuman = decrypt(id_pengumuman)
        data_kelas = m_kelas.objects.all()
        data_jenis_ujian = m_ujian.objects.all()
        data_mapel = m_mapel.objects.all()
        data_pengumuman = m_listpengumuman.objects.get(id_pengumuman = id_pengumuman)
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
            'data_pengumuman':data_pengumuman,
            'link':reverse('bimbel_app:edit_pengumuman', args=(encrypt(id_pengumuman),)),
        }
        return render(request, 'announce/create_pengumuman.html', data)

    def post(self, request, id_pengumuman):
        judul = request.POST.get('judul')
        tgl_terbit = request.POST.get('tgl_terbit')
        file = request.FILES.getlist('filenya')
        isi_materi = request.POST.get('isi_materi')
        arr_file = []

        tgl_terbit_ = datetime.strptime(tgl_terbit.split(' - ')[0], '%d/%m/%Y %H:%M')
        tgl_tutup = datetime.strptime(tgl_terbit.split(' - ')[1], '%d/%m/%Y %H:%M')


        for upload_file in file:
            rand_name = re.sub('[^\w\-_\. ]', '_', encrypt(str(datetime.now())))+random_string_angka()+' - '+upload_file.name.replace(' ','')

            file_path_ = os.path.join(BASE_DIR, 'bimbel_app', 'assets', 'doc_materi_temp', rand_name)
            with open(file_path_, 'wb+') as destination:
                for chunk in upload_file.chunks():
                    destination.write(chunk)

            dbx = dropbox.Dropbox(DBX_TOKEN)
            dbx.users_get_current_account()
            with open(file_path_, 'rb') as destination:
                dbx.files_upload(bytes(destination.read()), '/pengumuman/{}'.format(rand_name))
            arr_file.append(rand_name)
            os.remove(file_path_)

        pengumuman = m_listpengumuman.objects.get(id_pengumuman = decrypt(id_pengumuman))
        pengumuman.judul = judul
        pengumuman.isi_materi = isi_materi
        pengumuman.tgl_terbit_auto = tgl_terbit_
        pengumuman.tgl_tutup_auto = tgl_tutup
        
        if len(file) != 0:
            new_arr = pengumuman.file_support
            for x in arr_file:
                new_arr.append(x)
            pengumuman.file_support = new_arr
        pengumuman.user_input = m_user.objects.get(uid=global_var(request)['uid'])
        pengumuman.save()


        return redirect('bimbel_app:edit_pengumuman', id_pengumuman = id_pengumuman)

class change_stat_pengumumanView(View):
    """docstring for change_stat_materiView"""
    def post(self, request, status_):
        id_pengumuman = decrypt(request.POST.get('xx'))
        status = False

        try:
            data_pengumuman = m_listpengumuman.objects.get(id_pengumuman = id_pengumuman)
            data_pengumuman.status = status_
            data_pengumuman.save()
            status = True
        except Exception as e:
            print(e)
            status = False

        data = {
            'status':status,
        }
        return JsonResponse(data)

class del_file_pengumumanView(View):
    """docstring for change_stat_materiView"""
    def post(self, request):
        id_pengumuman = decrypt(request.POST.get('xx'))
        nama_file = request.POST.get('aa')
        status = False

        try:
            data_pengumuman = m_listpengumuman.objects.get(id_pengumuman = id_pengumuman)
            arra_list = data_pengumuman.file_support
            arra_list.remove(nama_file)
            data_pengumuman.file_support = arra_list
            
            data_pengumuman.save()

            dbx = dropbox.Dropbox(DBX_TOKEN)
            dbx.files_delete_v2('/pengumuman/{}'.format(nama_file))
            status = True
        except Exception as e:
            print(e)
            status = False

        data = {
            'status':status,
        }
        return JsonResponse(data)

class del_pengumumanView(View):
    """docstring for change_stat_materiView"""
    def post(self, request):
        id_pengumuman = decrypt(request.POST.get('vv'))
        status = False

        try:
            data_pengumuman = m_listpengumuman.objects.get(id_pengumuman = id_pengumuman)
            if data_pengumuman.user_input.uid == global_var(request)['uid'] or global_var(request)['level'].upper() == 'ADMIN':
                for x in data_pengumuman.file_support:
                    try:
                        dbx = dropbox.Dropbox(DBX_TOKEN)
                        dbx.files_delete_v2('/pengumuman/{}'.format(x))
                    except Exception as e:
                        print(e)
                        pass
                
                data_pengumuman.delete()
            status = True
        except Exception as e:
            print(e)
            status = False

        data = {
            'status':status,
        }
        return JsonResponse(data)

class lihat_pengumumanView(View):
    """docstring for lihat_materiView"""
    def get(self, request, id_pengumuman):
        id_pengumuman = decrypt(id_pengumuman)
        data_pengumuman = m_listpengumuman.objects.get(id_pengumuman=id_pengumuman)
        data_pengumuman_ = m_listpengumuman.objects.get(id_pengumuman=id_pengumuman)
        data_pengumuman_.count_see = data_pengumuman_.count_see+1

        try:
            data_pengumuman_.save()
        except Exception as e:
            print(e)
            pass

        data = {
            'data_pengumuman':data_pengumuman,
        }
        return render(request, 'announce/lihat_pengumuman.html', data)

        # if Helper.is_allowed_to_open(self, request, id_pengumuman, 'pengumuman'):
        #     try:
        #         data_materi_.save()
        #     except Exception as e:
        #         print(e)
        #         pass

        #     data = {
        #         'data_materi':data_materi,
        #     }
        #     return render(request, 'pengumuman/lihat_pengumuman.html', data)
        # else:
        #     if global_var(request)['level'].upper() == 'SISWA':
        #         messages.error(request, 'Materi Bukan Diperuntukan Untuk Kelas Anda. ')
        #         return redirect('bimbel_app:index')
        #     elif global_var(request)['level'].upper() == 'GURU':
        #         if data_materi.user_input.uid == global_var(request)['uid']:
        #             try:
        #                 data_materi_.save()
        #             except Exception as e:
        #                 print(e)
        #                 pass

        #             data = {
        #                 'data_materi':data_materi,
        #             }
        #             return render(request, 'materi/lihat_materi.html', data)
        #         else:
        #             messages.error(request, 'Tidak Diperkenankan Melihat. ')
        #             return redirect('bimbel_app:list_materi')
        
        
        
        