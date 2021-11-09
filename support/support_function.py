from django.db import connection,connections
from django.urls import reverse,resolve
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.template import RequestContext
from django.core.files import File
import re
import json
import os
import datetime

import gzip
import subprocess
import time
import pprint
import base64
import string
import random
from bimbel.settings import SESI
from bimbel_app.models.master import (Master_aplikasi as m_aplikasi)

monthList = {
    'Jan': 'Januari',
    'Feb': 'Februari',
    'Mar': 'Maret',
    'Apr': 'April',
    'May': 'Mei',
    'Jun': 'Juni',
    'Jul': 'Juli',
    'Aug': 'Agustus',
    'Sep': 'September',
    'Oct': 'Oktober',
    'Nov': 'November',
    'Dec': 'Desember'
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

def update_tgl(request):
    now = datetime.datetime.now()
    hari = datetime.datetime.now().strftime("%a")
    tanggal = datetime.datetime.now().strftime("%d")
    bulan = datetime.datetime.now().strftime("%b")
    tahunsaiki = datetime.datetime.now().strftime("%Y")
    tglblntahun = tanggal+' '+monthList[bulan]+' '+tahunsaiki

    tahunawal = datetime.datetime.now().date().replace(month=1, day=1)
    hari_awal = tahunawal.strftime("%a")
    tanggal_awal = tahunawal.strftime("%d")
    bulan_awal = tahunawal.strftime("%b")
    tahunsaiki_awal = tahunawal.strftime("%Y")

    # awal tahun mauludy
    tglblntahun_awal = tanggal_awal+' '+monthList[bulan_awal]+' '+tahunsaiki_awal
    # awal tahun mauludy
    tgl_lengkap = dayList[hari]+', '+tglblntahun
    tglblnThLog = tanggal+' '+monthList[bulan]

    return {"tgl_lengkap":tgl_lengkap,"tglblntahun":tglblntahun,"tahunsaiki":tahunsaiki,"tglblnThLog":tglblnThLog,"now":now}

def global_var(request):
    now = datetime.datetime.now()
    try:
        data_aplikasi = m_aplikasi.objects.get(jenis = 'aplikasi')
        nama_aplikasi = data_aplikasi.nama
    except Exception as e:
        data_aplikasi = ''
        nama_aplikasi = ''

    data = {
        'uid': request.session.get('uid_{}'.format(SESI)),
        'uidpd_': request.session.get('uidpd_{}'.format(SESI)),
        'uname': request.session.get(SESI),
        'level': request.session.get('level'),
        'fullname': request.session.get('fullname'),
        'tanggal_lengkap':update_tgl(request)['tgl_lengkap'],
        'tgl_now_to_db':now,
        'tahunsaiki':update_tgl(request)['tahunsaiki'],
        'nama_aplikasi':nama_aplikasi,
        'data_aplikasi':data_aplikasi,
    }
    return data

def random_string_angka(size=6, chars=string.ascii_uppercase + string.digits):
    random_ = ''.join(random.choice(chars) for _ in range(size))
    return random_

def get_time(request,now,last_activity):
    pecah1 = now.split(':')
    pecah2 = last_activity.split(':')

    waktu_sekarang = int(pecah1[1]) + 60*int(pecah1[0])
    waktu_terakhir = int(pecah2[1]) + 60*int(pecah2[0])
    selisih = ((waktu_sekarang-waktu_terakhir)**2)**0.5
    return selisih

# encrypt decrypt
def decode_base64(data):
    missing_padding = len(data) % 4    
    if missing_padding != 0:
        data += b'='* (4 - missing_padding)    
    return base64.decodebytes(data.encode())

def decrypt(isi,key='%yudhigantengsekali&'):
    i = 1
    hsl = ''
    s = decode_base64(isi)
    #print s
    for i in range(len(s)):
        char = s[i:i+1]

        ordchar = ord(char)
        hs = (i % len(isi))-1
        if i == len(key):
            hs = 9
        elif i> len(key):
            hs = (i-len(key) % len(isi)-1)

        if hs == -1:
            hs = len(key)-1

        keychar = key[hs:hs+1]
        ordkeychar = ord(keychar)
        jml = ordchar - ordkeychar
        char = chr(jml)
        hsl += char

    return str(hsl)

def encrypt(isi,key='%yudhigantengsekali&'):
    i = 1
    hsl = ''
    s = isi
    #print s
    for i in range(len(s)):
        char = s[i:i+1]

        ordchar = ord(char)
        hs = (i % len(isi))-1
        if i == len(key):
            hs = 9
        elif i> len(key):
            hs = (i-len(key) % len(isi)-1)

        if hs == -1:
            hs = len(key)-1

        keychar = key[hs:hs+1]
        ordkeychar = ord(keychar)
        jml = ordchar + ordkeychar
        char = chr(jml)
        hsl += char     
    return base64.b64encode(hsl.encode('latin',errors = 'ignore')).decode('ascii')