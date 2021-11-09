from django import template
from support.support_function import encrypt, decrypt, random_string_angka
from bimbel_app.models.master import (Master_kelas as m_kelas)
from bimbel_app.views.ujian_views import Helper
from bimbel.settings import DBX_TOKEN
import dropbox

register = template.Library()

def encrypt_this(value):
    return encrypt(str(value))

def random_string_encrypt(value):
    return encrypt(str(random_string_angka()))

def decrypt_this(value):
    return decrypt(str(value))

def get_nama_kelas(value):
	arr = []
	for x in value:
		data_kelas = m_kelas.objects.get(kode_kelas = x)
		arr.append(data_kelas.nama_kelas)
	return arr

def get_link_dbx_file(value):
    dbx = dropbox.Dropbox(DBX_TOKEN)
    result = dbx.files_get_temporary_link('/materi/{}'.format(value))

def get_link_dbx_file_pengumuman(value):
    dbx = dropbox.Dropbox(DBX_TOKEN)
    result = dbx.files_get_temporary_link('/pengumuman/{}'.format(value))

    return result.link
# @register.inclusion_tag('ujian/list_ujian_siswa.html', takes_context=True)
def is_still_available_form(values, request):
    # request = context['request']
    return Helper().is_still_available(request, values)

def get_nilai_siswa(values, request):
    return Helper().get_nilai_siswa(request, values)

@register.simple_tag
def get_nilai_siswa_batch(values, request, siswa):
    return Helper().get_nilai_siswa_batch(request, values, siswa)

@register.simple_tag
def is_passing(values, request, id_ujian):
    
    return Helper().get_is_passing(request, values, id_ujian)

monthList = {
    '01': 'Januari',
    '02': 'Februari',
    '03': 'Maret',
    '04': 'April',
    '05': 'Mei',
    '06': 'Juni',
    '07': 'Juli',
    '08': 'Agustus',
    '09': 'September',
    '10': 'Oktober',
    '11': 'November',
    '12': 'Desember'
}
dayList = {
    'Sun' : 'Minggu',
    'Mon' : 'Senin',
    'Tue' : 'Selasa',
    'Wed' : 'Rabu',
    'Thu' : 'Kamis',
    'Fri' : 'Jumat',
    'Sat' : 'Sabtu'
}

def to_tgl_indo_with_time(value):
	tgl__ = ''
	value = value.strftime("%d-%m-%Y %H:%M:%S")
	# 2021-04-12 08:00:00
	try:
		tgl = value.split(' ')[0]
		waktu = value.split(' ')[1]
		bulan = monthList[tgl.split('-')[1]]
		tgl__ = '{} {} {} {}'.format(tgl.split('-')[0],bulan,tgl.split('-')[2],waktu)
	except Exception as e:
		print(e)

	return tgl__

def add_by_one(value):
    return int(value)+1

def get_filename(value):
    return value.split(' - ')[1]

import re

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext
    
register.filter('encrypt_this', encrypt_this)
register.filter('decrypt_this', decrypt_this)
register.filter('get_nama_kelas', get_nama_kelas)
register.filter('add_by_one', add_by_one)
register.filter('to_tgl_indo_with_time', to_tgl_indo_with_time)
register.filter('is_still_available_form', is_still_available_form)
register.filter('get_nilai_siswa', get_nilai_siswa)
register.filter('random_string_encrypt', random_string_encrypt)
register.filter('get_link_dbx_file', get_link_dbx_file)
register.filter('get_filename', get_filename)
register.filter('get_nilai_siswa_batch', get_nilai_siswa_batch)
register.filter('is_passing', is_passing)
register.filter('get_link_dbx_file_pengumuman', get_link_dbx_file_pengumuman)
register.filter('cleanhtml', cleanhtml)
    
