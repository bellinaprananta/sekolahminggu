from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from django.contrib import messages

from django.forms import *
from bimbel_app.models.master import (Master_user as m_user, Peserta_didik as m_pd, List_ujian as m_listujian, List_materi as m_listmateri, Master_guru as m_guru
                                        ,Master_aplikasi as m_aplikasi, List_pengumuman as m_listpengumuman)
from support.support_function import decrypt, encrypt, global_var
from bimbel.settings import SESI
from django.db.models import Q
from bimbel_app.views.kesiswaan_views import tambah_siswaView

class IndexView(View):
    """docstring for ClassName"""
    def get(self, request):
        data_siswa = ''
        data_list_ujian = ''
        data_list_materi = ''
        data_guru = ''
        jml_ujian = 0
        
        jml_siswa = m_pd.objects.filter(status = 'Y').count()
        jml_siswa_baru = m_pd.objects.filter(status = 'N').count()
        jml_ujian_ = m_listujian.objects.all().count()
        jml_materi = m_listmateri.objects.all().count()

        data_pengumuman = m_listpengumuman.objects.all()

        if global_var(request)['level'] == 'SISWA':
            data_siswa = m_pd.objects.get(uid=global_var(request)['uidpd_'])
            data_list_ujian = m_listujian.objects.filter(
                                Q(kelas='all') | 
                                Q(kelas='certain', daftar_kelas__contains = [data_siswa.kelas.kode_kelas]) |
                                Q(Q(kelas='except'), ~Q(daftar_kelas__contains = [data_siswa.kelas.kode_kelas])),
                                status__in = ['TERBIT', 'TUTUP']
                                )[:5]
            jml_ujian = m_listujian.objects.filter(
                                Q(kelas='all') | 
                                Q(kelas='certain', daftar_kelas__contains = [data_siswa.kelas.kode_kelas]) |
                                Q(Q(kelas='except'), ~Q(daftar_kelas__contains = [data_siswa.kelas.kode_kelas])),
                                status__in = ['TERBIT', 'TUTUP']
                                ).count()

            data_list_materi = m_listmateri.objects.filter(
                                Q(kelas='all') | 
                                Q(kelas='certain', daftar_kelas__contains = [data_siswa.kelas.kode_kelas]) |
                                Q(Q(kelas='except'), ~Q(daftar_kelas__contains = [data_siswa.kelas.kode_kelas])),
                                status__in = ['TERBIT', 'TUTUP']
                                )[:5]
        elif global_var(request)['level'] == 'GURU':
            data_guru = m_guru.objects.get(uid=global_var(request)['uidpd_'])
            data_list_materi = m_listmateri.objects.filter(
                                status__in = ['TERBIT', 'TUTUP'], user_input = global_var(request)['uid']
                                )[:5]
        data = {
            'data_siswa':data_siswa, 
            'data_list_ujian':data_list_ujian,
            'jml_ujian':jml_ujian,
            'data_list_materi':data_list_materi,
            'jml_siswa' : jml_siswa,
            'jml_siswa_baru' : jml_siswa_baru,
            'jml_ujian_' : jml_ujian_,
            'jml_materi' : jml_materi,
            'data_guru':data_guru,
            'data_pengumuman':data_pengumuman,

        }
        return render(request, 'base/home.html', data)

class join_video_confView(View):
    """docstring for join_chat"""
    def post(self, request):
        uname = json.loads(request.body)['uname']
        token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY_SID,
                        TWILIO_API_KEY_SECRET, identity=uname)
        token.add_grant(VideoGrant(room='My Room'))
        # print(token.to_jwt().decode())
        data = {
            'token': token.to_jwt().decode(),
        }
        return JsonResponse(data)

class LogoutView(View):
    """docstring for LogoutView"""

    def get(self, request):
        # update_status_logged = m_user.objects.get(uname=global_var(request)['uname'])
        # update_status_logged.is_logged = 'T'
        # update_status_logged.save()

        request.session.flush()

        messages.success(request, "Anda telah berhasil Log out.")
        return HttpResponseRedirect('bimbel_app:login')

class LoginView(View):
    def get(self, request):
        form = LoginForm()

        data = {
            'form':form,
        }
        return render(request, 'base/login.html', data)
    
    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            uname = form.cleaned_data.get('uname')
            pwd = form.cleaned_data.get('pwd')

            is_exists = m_user.objects.filter(uname=uname, pwd = encrypt(pwd)).count()
            if int(is_exists) == 1:
                user_data = m_user.objects.filter(uname=uname, pwd = encrypt(pwd)).values('uid', 'nip', 'uname', 'fullname', 'level')
                user_pd = m_pd.objects.filter(email=uname).values('uid')
                # if user_data.values()[0]['is_logged'] == 'Y':
                #     messages.error(request, 'User Ada Masih Tertaut Pada Device Lain. Silahkan LOGOUT Terlebih Dahulu. ')
                #     return redirect('bimbel_app:login')
                # else:
                
                request.session['next'] = 'jancuk'
                request.session[SESI] = uname
                request.session['uid_{}'.format(SESI)] = user_data[0]['uid']

                if user_data[0]['level'] in ['SISWA']:
                    request.session['uidpd_{}'.format(SESI)] = user_pd[0]['uid']
                elif user_data[0]['level'] in ['GURU']:
                    user_pd = m_guru.objects.filter(email=uname).values('uid')
                    request.session['uidpd_{}'.format(SESI)] = user_pd[0]['uid']

                request.session['level'] = user_data[0]['level']
                request.session['fullname'] = user_data[0]['fullname']
                messages.success(request, 'Selamat Datang, {}'.format(user_data[0]['fullname'].upper()))

                # update_status_logged = m_user.objects.get(uname=uname, pwd = encrypt(pwd))
                # update_status_logged.is_logged = 'Y'
                # update_status_logged.save()
                return redirect('bimbel_app:index')
            else:
                messages.error(request, 'User Tidak Ditemukan')
                return redirect('bimbel_app:login')

        return redirect('bimbel_app:login')

class LoginForm(Form):
    uname = CharField(widget=TextInput(attrs={'class':'form-control pl-15 bg-transparent','required':'required', 'placeholder':'Username'}))
    pwd = CharField(widget=PasswordInput(attrs={'class':'form-control pl-15 bg-transparent','required':'required', 'placeholder':'Password'}))
        
        

class setting_aplikasiView(View):
    """docstring for setting_aplikasiView"""
    def get(self, request):
        data_aplikasi = ''
        
        try:
            data_aplikasi = m_aplikasi.objects.get(jenis = 'aplikasi')
        except Exception as e:
            pass
        data = {
            'data_aplikasi':data_aplikasi,
        }
        return render(request, 'base/modal/modal_pengaturan.html', data)
    def post(self, request):
        nama = request.POST.get('nama_siswa')
        alamat = request.POST.get('alamat')
        no_hp = request.POST.get('nohp')
        foto = request.FILES.get('foto')
        email = request.POST.get('email')
        
        if foto != None:
            tambah_siswaView().write_image('logo_aplikasi.png', foto)


        m_aplikasi_ = m_aplikasi(
                jenis = 'aplikasi',
                nama = nama,
                alamat = alamat, 
                no_hp = no_hp, 
                foto = 'logo_aplikasi.png', 
                email = email, 
                user_input = m_user.objects.get(uid = global_var(request)['uid']),
                )
        m_aplikasi_.save()
        return redirect('bimbel_app:logout')
        
# Create your views here.
