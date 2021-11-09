from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json, os
from django.contrib import messages
from bimbel_app.models.master import (Master_user as m_user, Master_mata_pelajaran as m_mapel, Master_guru as m_guru, Master_kelas as m_kelas)
from django.forms import *
from support.support_function import decrypt, encrypt, global_var, random_string_angka
from bimbel.settings import BASE_DIR
import re
from django.urls import reverse
# from PIL import Image

class guruView(View):
    """docstring for PesertaDidikView"""
    def get(self, request):
        data_siswa = m_guru.objects.all()
        data = {
            'data_siswa':data_siswa, 
        }
        return render(request, 'pengajar/guru.html', data)

class tambah_guruView(View):

    def write_image(self, rand_name, foto):
        status_write = False
        try:
            pict_path = os.path.join(BASE_DIR, 'bimbel_app', 'assets', 'images', 'f_profil', rand_name)
            with open(pict_path, 'wb+') as destination:
                for chunk in foto.chunks():
                    destination.write(chunk)
            status_write = True
        except Exception as e:
            print('djancuk', e)
            status_write = False

        return status_write
    """docstring for tambah_siswaView"""
    def get(self, request, type_, uid):
        data_kelas = m_kelas.objects.all()
        data_siswa = ''
        data_login = ''
        uuid = 0

        if type_ == 'edit':
            data_siswa = m_guru.objects.filter(uid=uid).values()
            data_login = m_user.objects.filter(uname=data_siswa[0]['email']).values_list('pwd')
            data_login = decrypt(data_login[0][0])
            uuid = uid
        data = {
            'data_kelas':data_kelas,
            'type_':type_, 
            'data_siswa':data_siswa,
            'data_login':data_login,
            'uuid':uid,
            'link':reverse('bimbel_app:tambah_guru', args=(type_,uid)),
        }
        return render(request, 'pengajar/modal/add_edit_guru.html', data)

    def post(self, request, type_, uid):
        nama_guru = request.POST.get('nama_guru')
        nip = request.POST.get('nip')
        jenis_kelamin = request.POST.get('jenis_kelamin')
        tempat_lahir = request.POST.get('tempat_lahir')
        tanggal_lahir = request.POST.get('tgl_lahir')
        alamat = request.POST.get('alamat')
        agama = request.POST.get('agama')
        no_hp = request.POST.get('nohp')
        tahun_registrasi = global_var(request)['tahunsaiki']
        status = 'Y'
        informasi_lain = request.POST.get('informasi_lain')
        foto = request.FILES.get('foto')
        email = request.POST.get('email')
        user_input = m_user.objects.get(uid = global_var(request)['uid'])
        password = request.POST.get('password')

        rand_name = re.sub('[^\w\-_\. ]', '_', encrypt('Aditya Yudhi Hanafi'))+random_string_angka()+'.jpg'

        if type_ == 'add':
            if self.write_image(rand_name, foto):
                data_login = m_user(
                    uname = email,
                    pwd = encrypt(password),
                    fullname = nama_guru,
                    nip = nip,
                    level = 'GURU',
                    )
                data_login.save()

                data_siswa =  m_guru(
                        nama_guru = nama_guru,
                        nip = nip, 
                        jenis_kelamin = jenis_kelamin, 
                        tempat_lahir = tempat_lahir, 
                        tanggal_lahir = tanggal_lahir,
                        alamat = alamat,
                        agama = agama, 
                        no_hp = no_hp, 
                        tahun_registrasi = tahun_registrasi, 
                        status = status, 
                        informasi_lain = informasi_lain,
                        foto = rand_name,
                        email = email,
                        user_input = user_input,
                        )
                data_siswa.save()
            messages.success(request, 'Edit Peserta Didik Sukses !')

        elif type_ == 'edit':
            data_siswa = m_guru.objects.get(uid=uid)
            data_login = m_user.objects.get(uname=data_siswa.email)

            status_write = False
            is_foto_edited = False
            if foto != None:
                status_write = self.write_image(rand_name, foto)
                os.remove(os.path.join(BASE_DIR, 'bimbel_app', 'assets', 'images', 'f_profil', data_siswa.foto))
                is_foto_edited = True
            else:
                status_write = True
                is_foto_edited = False

            if status_write:                
                if data_siswa.email != email:
                    data_login.uname = email
                    data_login.save()

                if data_siswa.email != encrypt(password):
                    data_login.pwd = encrypt(password)
                    data_login.save()

                if data_siswa.nama_guru != nama_guru:
                    data_login.fullname = nama_guru
                    data_login.save()

                if data_siswa.nip != nip:
                    data_login.nip = nip
                    data_login.save()

                data_siswa.nama_guru = nama_guru
                data_siswa.nip = nip
                data_siswa.jenis_kelamin = jenis_kelamin 
                data_siswa.tempat_lahir = tempat_lahir 
                data_siswa.tanggal_lahir = tanggal_lahir
                data_siswa.alamat = alamat
                data_siswa.agama = agama 
                data_siswa.no_hp = no_hp 
                data_siswa.tahun_registrasi = tahun_registrasi 
                data_siswa.status = status 
                data_siswa.informasi_lain = informasi_lain

                if is_foto_edited:
                    data_siswa.foto = rand_name

                data_siswa.email = email
                data_siswa.user_input = user_input

                data_siswa.save()

            messages.success(request, 'Edit Peserta Didik Sukses !')
        else:
            messages.error(request, 'Tambah Peserta Didik Gagal !')
        data = {}

        return redirect('bimbel_app:guru')

class DeleteSiswaViews(View):
    """docstring for DeleteBarang"""
    def post(self, request, uid):
        status = False
        data_siswa = m_guru.objects.filter(uid=uid)
        data_user = m_user.objects.filter(uname=data_siswa.values()[0]['email'])
        status_delete = False
        try:
            os.remove(os.path.join(BASE_DIR, 'bimbel_app', 'assets', 'images', 'f_profil', data_siswa.values()[0]['foto']))
            status_delete = True
        except Exception as e:
            print('error hapus foto', e)
            status_delete = False

        if status_delete:
            try:
                data_siswa.delete()
                data_user.delete()
                status = True
            except Exception as e:
                print(e)
                status = False

        data = {
            'status':status,
        }
        return JsonResponse(data)

class ValidationLoginSiswaViews(View):
    """docstring for ValidationLoginSiswaViews"""
    def post(self, request):
        status = False
        uname = request.POST.get('uname')
        count_login = m_user.objects.filter(uname=uname).count()
        print(count_login)
        if count_login == 0:
            status = True
        else:
            status = False

        data = {
            'status':status,
        }
        return JsonResponse(data)

class profil_guruView(View):

    def write_image(self, rand_name, foto):
        status_write = False
        try:
            pict_path = os.path.join(BASE_DIR, 'bimbel_app', 'assets', 'images', 'f_profil', rand_name)
            with open(pict_path, 'wb+') as destination:
                for chunk in foto.chunks():
                    destination.write(chunk)
            status_write = True
        except Exception as e:
            print('djancuk', e)
            status_write = False

        return status_write

    def get(self, request, type_, uid):
        uid = int(decrypt(uid))

        data_kelas = m_kelas.objects.all()
        data_siswa = ''
        data_login = ''
        uuid = 0

        if type_ == 'edit':
            data_siswa = m_guru.objects.filter(uid=uid).values()
            data_login = m_user.objects.filter(uname=data_siswa[0]['email']).values_list('pwd')
            data_login = decrypt(data_login[0][0])
            uuid = uid
        data = {
            'data_kelas':data_kelas,
            'type_':type_, 
            'data_siswa':data_siswa,
            'data_login':data_login,
            'uuid':uid,
            'link':reverse('bimbel_app:profil_guru', args=(type_,encrypt(str(uid))))
        }
        return render(request, 'pengajar/modal/add_edit_guru.html', data)

    def post(self, request, type_, uid):
        uid = int(decrypt(uid))

        nama_guru = request.POST.get('nama_guru')
        nip = request.POST.get('nip')
        jenis_kelamin = request.POST.get('jenis_kelamin')
        tempat_lahir = request.POST.get('tempat_lahir')
        tanggal_lahir = request.POST.get('tgl_lahir')
        alamat = request.POST.get('alamat')
        agama = request.POST.get('agama')
        no_hp = request.POST.get('nohp')
        tahun_registrasi = global_var(request)['tahunsaiki']
        status = 'Y'
        informasi_lain = request.POST.get('informasi_lain')
        foto = request.FILES.get('foto')
        email = request.POST.get('email')
        user_input = m_user.objects.get(uid = global_var(request)['uid'])
        password = request.POST.get('password')

        rand_name = re.sub('[^\w\-_\. ]', '_', encrypt('Aditya Yudhi Hanafi'))+random_string_angka()+'.jpg'

        if type_ == 'edit':
            data_siswa = m_guru.objects.get(uid=uid)
            data_login = m_user.objects.get(uname=data_siswa.email)

            status_write = False
            is_foto_edited = False
            if foto != None:
                status_write = self.write_image(rand_name, foto)
                os.remove(os.path.join(BASE_DIR, 'bimbel_app', 'assets', 'images', 'f_profil', data_siswa.foto))
                is_foto_edited = True
            else:
                status_write = True
                is_foto_edited = False

            if status_write:                
                if data_siswa.email != email:
                    data_login.uname = email
                    data_login.save()

                if data_siswa.email != encrypt(password):
                    data_login.pwd = encrypt(password)
                    data_login.save()

                if data_siswa.nama_guru != nama_guru:
                    data_login.fullname = nama_guru
                    data_login.save()

                if data_siswa.nip != nip:
                    data_login.nip = nip
                    data_login.save()

                data_siswa.nama_guru = nama_guru
                data_siswa.nip = nip
                data_siswa.jenis_kelamin = jenis_kelamin 
                data_siswa.tempat_lahir = tempat_lahir 
                data_siswa.tanggal_lahir = tanggal_lahir
                data_siswa.alamat = alamat
                data_siswa.agama = agama 
                data_siswa.no_hp = no_hp 
                data_siswa.tahun_registrasi = tahun_registrasi 
                data_siswa.status = status 
                data_siswa.informasi_lain = informasi_lain

                if is_foto_edited:
                    data_siswa.foto = rand_name

                data_siswa.email = email
                data_siswa.user_input = user_input

                data_siswa.save()

            messages.success(request, 'Edit Profil Sukses !')
        else:
            messages.error(request, 'Tambah Peserta Didik Gagal !')

        return redirect('bimbel_app:index')


        
        
