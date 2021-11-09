from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from django.contrib import messages
from bimbel_app.models.master import (Master_user as m_user, Master_mata_pelajaran as m_mapel, Master_kelas as m_kelas, Master_ujian as m_ujian)
from django.forms import *
from support.support_function import decrypt, encrypt, global_var
from django.db import IntegrityError
from django.db.models import ProtectedError

class UsermanagementView(View):
    """docstring for UsermanagementView"""
    def get(self, request):
        data_user = m_user.objects.all()
        form = UserForm()

        data = {
            'data_user':data_user,
            'form':form,
        }
        return render(request, 'master/usermanagement.html', data)

    def post(self, request):
        form = UserForm(request.POST)

        if form.is_valid():
            uname = form.cleaned_data.get('uname')
            pwd = form.cleaned_data.get('pwd')
            level = form.cleaned_data.get('level')
            fullname = form.cleaned_data.get('fullname')
            nip = form.cleaned_data.get('nip')

            try:
                jml_user = m_user.objects.get(uname = uname)
                messages.error(request, "User Gagal Ditambahkan. Username Sudah Ada.")
            except Exception as e:
                a = form.save(commit=False)
                a.pwd = encrypt(pwd)
                a.uname = uname.replace(' ','')

                form.save()

                messages.success(request, "User Berhasil Ditambahkan. ")                
        else:
            messages.error(request, "User Gagal Ditambahkan. Pastikan Semua Isian Terisi dan Username Belum Pernah Digunakan.")
        return redirect('bimbel_app:usermanagement')

class UsermanagementEditView(View):
    """docstring for UsermanagementEditView"""
    def get(self, request, uid):
        uid = decrypt(uid)
        level = ''
        data_user = m_user.objects.filter(uid=uid).values('uname', 'nip', 'level', 'fullname')
        level = m_user.objects.get(uid=uid).level
        data = {
            'data_user': list(data_user),
            'level':level,
        }
        return JsonResponse(data)
    def post(self, request, uid):
        uid = decrypt(uid)
        data_user = m_user.objects.get(uid=uid)
        level = m_user.objects.get(uid=uid).level

        if level == 'SISWA':
            messages.error(request, 'Silahkan Edit Melalui Menu Kesiswaan > Peserta Didik. ')
            return redirect('bimbel_app:usermanagement')
        elif level == 'GURU':
            messages.error(request, 'Silahkan Edit Melalui Menu Guru. ')
            return redirect('bimbel_app:usermanagement')
        else:
            data_user.uname = request.POST.get('uname').replace(' ','')
            
            data_user.level = request.POST.get('level')
            data_user.fullname = request.POST.get('fullname')
            data_user.nip = request.POST.get('nip')
            
            form = UserFormEdit(request.POST, instance = data_user)
            form.save()

            messages.success(request, 'Edit User Berhasil. ')
        
            return redirect('bimbel_app:usermanagement')

class UsermanagementDeleteView(View):
    """docstring for UsermanagementDeleteView"""
    def post(self, arg, uid):
        uid = decrypt(uid)
        status = False
        level = ''

        try:
            data_user = m_user.objects.get(uid=uid)
            if data_user.level == 'SISWA':
                status = False
            elif data_user.level == 'GURU':
                status = False
            else:
                m_user.objects.filter(uid=uid).delete()
                status = True
            level = data_user.level
        except Exception as e:
            status = False
        data = {
            'status':status,
            'level':level,
        }
        return JsonResponse(data)
        

class UserFormEdit(ModelForm):
    class Meta:
        model = m_user
        fields = ['uname', 'level', 'fullname', 'nip']

class UserForm(ModelForm):
    class Meta:
        model = m_user
        fields = ['uname', 'pwd', 'level', 'fullname', 'nip']

    def get_choices():
        return (('ADMIN', 'ADMIN'),)

    uname = CharField(widget=TextInput(attrs={'class':'form-control form-control-user','required':'required', 'placeholder':'Username'}), required=False)
    pwd = CharField(widget=PasswordInput(attrs={'class':'form-control form-control-user','required':'required', 'placeholder':'Password'}), required=False)
    fullname = CharField(widget=TextInput(attrs={'class':'form-control form-control-user','required':'required', 'placeholder':'Nama Lengkap'}))
    level = ChoiceField(choices=get_choices, widget=Select(attrs={'class':'form-control', 'id':'select_hakakses'}))
    nip = CharField(widget=TextInput(attrs={'class':'form-control form-control-user','required':'required', 'placeholder':'NIP'}))

# MATA PELAJARAN
class MapelView(View):
    """docstring for MapelView"""
    def get(self, request):
        data_mapel = m_mapel.objects.all()
        form = MapelForm()

        data = {
            'data_mapel':data_mapel,
            'form':form,
        }
        return render(request, 'master/mapel.html', data)

    def post(self, request):
        form = MapelForm(request.POST)
        if form.is_valid():
            kode_mapel = form.cleaned_data.get('kode_mapel')
            nama_mapel = form.cleaned_data.get('nama_mapel')

            a = form.save(commit=False)
            a.kode_mapel = kode_mapel.replace(' ','')
            a.nama_mapel = nama_mapel
            a.user_input = m_user.objects.get(uid = global_var(request)['uid'])

            form.save()

            messages.success(request, "Mata Pelajaran Berhasil Ditambahkan. ")
        else:
            messages.error(request, "Mata Pelajaran Gagal Ditambahkan. Kode Sudah Ada. ")
        return redirect('bimbel_app:mapel')

class MapelForm(ModelForm):
    class Meta:
        model = m_mapel
        fields = ['kode_mapel', 'nama_mapel']

    kode_mapel = CharField(widget=TextInput(attrs={'class':'form-control form-control-user','required':'required', 'placeholder':'Kode Mata Pelajaran'}), required=False)
    nama_mapel = CharField(widget=TextInput(attrs={'class':'form-control form-control-user','required':'required', 'placeholder':'Nama Mata Pelajaran'}), required=False)

class MapelFormEdit(ModelForm):
    class Meta:
        model = m_mapel
        fields = ['nama_mapel']


class MapelEditView(View):
    """docstring for UsermanagementEditView"""
    def get(self, request, kode_mapel):
        data_mapel = m_mapel.objects.filter(kode_mapel=kode_mapel).values('nama_mapel')

        data = {
            'data_mapel': list(data_mapel),
        }
        return JsonResponse(data)

    def post(self, request, kode_mapel):
        data_mapel = m_mapel.objects.get(kode_mapel=kode_mapel)
        
        data_mapel.nama_mapel = request.POST.get('nama_mapel').replace(' ','')
        
        form = MapelFormEdit(request.POST, instance = data_mapel)
        
        form.save()
        messages.success(request, 'Edit Mata Pelajaran Berhasil. ')
        
        return redirect('bimbel_app:mapel')

class MapelDeleteView(View):
    """docstring for UsermanagementDeleteView"""
    def post(self, arg, kode_mapel):
        status = False
        is_affiliate = False

        try:
            m_mapel.objects.filter(kode_mapel=kode_mapel).delete()
            status = True
        except ProtectedError as protec_error:
            is_affiliate = True
            status = False
        except Exception as e:
            status = False
        data = {
            'status':status,
            'is_affiliate':is_affiliate,
        }
        return JsonResponse(data)

# KELAS
class KelasView(View):
    """docstring for KelasView"""
    def get(self, request):
        data_kelas = m_kelas.objects.all()
        form = KelasForm()

        data = {
            'data_kelas':data_kelas,
            'form':form,
        }
        return render(request, 'master/kelas.html', data)

    def post(self, request):
        form = KelasForm(request.POST)
        if form.is_valid():
            kode_kelas = form.cleaned_data.get('kode_kelas')
            nama_kelas = form.cleaned_data.get('nama_kelas')

            a = form.save(commit=False)
            a.kode_kelas = kode_kelas.replace(' ','')
            a.nama_kelas = nama_kelas
            a.user_input = m_user.objects.get(uid = global_var(request)['uid'])

            form.save()

            messages.success(request, "Kelas Berhasil Ditambahkan. ")
        else:
            messages.error(request, "Kelas Gagal Ditambahkan. Kode Sudah Ada.")
        return redirect('bimbel_app:kelas')

class KelasForm(ModelForm):
    class Meta:
        model = m_kelas
        fields = ['kode_kelas', 'nama_kelas']

    kode_kelas = CharField(widget=TextInput(attrs={'class':'form-control form-control-user','required':'required', 'placeholder':'Kode Kelas'}), required=False)
    nama_kelas = CharField(widget=TextInput(attrs={'class':'form-control form-control-user','required':'required', 'placeholder':'Nama Kelas'}), required=False)

class KelasFormEdit(ModelForm):
    class Meta:
        model = m_kelas
        fields = ['nama_kelas']


class KelasEditView(View):
    """docstring for UsermanagementEditView"""
    def get(self, request, kode_kelas):
        data_kelas = m_kelas.objects.filter(kode_kelas=kode_kelas).values('nama_kelas')

        data = {
            'data_kelas': list(data_kelas),
        }
        return JsonResponse(data)

    def post(self, request, kode_kelas):
        data_kelas = m_kelas.objects.get(kode_kelas=kode_kelas)
        
        data_kelas.nama_kelas = request.POST.get('nama_kelas').replace(' ','')
        
        form = KelasFormEdit(request.POST, instance = data_kelas)
        
        form.save()
        messages.success(request, 'Edit Kelas Berhasil. ')
        
        return redirect('bimbel_app:kelas')

class KelasDeleteView(View):
    """docstring for UsermanagementDeleteView"""
    def post(self, arg, kode_kelas):
        status = False
        is_affiliate = False

        try:
            m_kelas.objects.filter(kode_kelas=kode_kelas).delete()
            status = True
        except ProtectedError as protec_error:
            is_affiliate = True
            status = False
        except Exception as e:
            status = False
        data = {
            'status':status,
            'is_affiliate':is_affiliate,
        }
        return JsonResponse(data)

# KATEGORI UJIAN
class kategori_ujianView(View):
    """docstring for KelasView"""
    def get(self, request):
        data_ujian = m_ujian.objects.all()
        form = ujianForm()

        data = {
            'data_ujian':data_ujian,
            'form':form,
        }
        return render(request, 'master/kategori_ujian.html', data)

    def post(self, request):
        form = ujianForm(request.POST)
        if form.is_valid():
            kode_ujian = form.cleaned_data.get('kode_ujian')
            nama_ujian = form.cleaned_data.get('nama_ujian')

            a = form.save(commit=False)
            a.kode_ujian = kode_ujian.replace(' ','')
            a.nama_ujian = nama_ujian
            a.user_input = m_user.objects.get(uid = global_var(request)['uid'])

            form.save()

            messages.success(request, "ujian Berhasil Ditambahkan. ")
        else:
            messages.error(request, "ujian Gagal Ditambahkan. Kode Sudah Ada.")
        return redirect('bimbel_app:kategori_ujian')

class ujianForm(ModelForm):
    class Meta:
        model = m_ujian
        fields = ['kode_ujian', 'nama_ujian']

    kode_ujian = CharField(widget=TextInput(attrs={'class':'form-control form-control-user','required':'required', 'placeholder':'Kode ujian'}), required=False)
    nama_ujian = CharField(widget=TextInput(attrs={'class':'form-control form-control-user','required':'required', 'placeholder':'Nama ujian'}), required=False)

class ujianFormEdit(ModelForm):
    class Meta:
        model = m_ujian
        fields = ['nama_ujian']


class kategori_ujianEditView(View):
    """docstring for UsermanagementEditView"""
    def get(self, request, kode_ujian):
        data_ujian = m_ujian.objects.filter(kode_ujian=kode_ujian).values('nama_ujian')

        data = {
            'data_ujian': list(data_ujian),
        }
        return JsonResponse(data)

    def post(self, request, kode_ujian):
        data_ujian = m_ujian.objects.get(kode_ujian=kode_ujian)
        
        data_ujian.nama_ujian = request.POST.get('nama_ujian').replace(' ','')
        
        form = ujianFormEdit(request.POST, instance = data_ujian)
        
        form.save()
        messages.success(request, 'Edit Ujian Berhasil. ')
        
        return redirect('bimbel_app:kategori_ujian')

class kategori_ujianDeleteView(View):
    """docstring for UsermanagementDeleteView"""
    def post(self, arg, kode_ujian):
        status = False
        is_affiliate = False

        try:
            m_ujian.objects.filter(kode_ujian=kode_ujian).delete()
            status = True
        except ProtectedError as protec_error:
            is_affiliate = True
            status = False
        except Exception as e:
            status = False
        data = {
            'status':status,
            'is_affiliate':is_affiliate,
        }
        return JsonResponse(data)


        

        
        