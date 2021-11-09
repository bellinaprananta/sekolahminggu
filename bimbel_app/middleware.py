from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db import connection
from django.test import TestCase, override_settings
from support.support_function import get_time, encrypt
from django.contrib.auth.models import User
from bimbel.settings import SESI, ALLOWED_HOSTS, STATIC_URL

import datetime

def cek_user(get_response):
    def middleware(request):
        if request.path == '/':
            return HttpResponseRedirect(reverse('bimbel_app:index'))
        else:
            response = get_response(request)

            if(request.session.get('next')):
                if request.get_host() in ALLOWED_HOSTS:
                    request.session['username_final'] = request.session.get(SESI,'')
                else:
                    messages.error(request, 'Connection Blocked, Please Contact Admin')
            
            # if request.session.get('telo') == 'telo' and request.path != reverse('bimbel_app:user_config') and request.path != reverse('bimbel_app:login'):
            #     return HttpResponseRedirect(reverse('bimbel_app:user_config')) 
            # elif not request.session.get('username_final','') and request.path not in [reverse('bimbel_app:login'), reverse('bimbel_app:user_config'), reverse('apirest_get')]:
            if not request.session.get('username_final','') and request.path not in [reverse('bimbel_app:login')] and not request.path.startswith(STATIC_URL) and not request.path.startswith('/report'):
                return HttpResponseRedirect(reverse('bimbel_app:login'))
            else:
                # activate if you wanna use inactive session time limit for 1 hour
                # now = datetime.datetime.now().strftime('%H:%M:%S')
                # last_activity = request.session.get('last_login_timestamp','00:00:00')

                # if(request.session.get('username_final')):
                #     menus = ['/dash/','/dash/logout/']

                #     if(request.path in ['/dash/login/']):
                #         print('djancuk2')
                #         return HttpResponseRedirect(reverse('bimbel_app:index'))

                # selisih = get_time(request,now,last_activity)
        
                # if selisih>=100 and request.path not in ['/dash/login/'] and not request.path.startswith(STATIC_URL) and not request.path.startswith('/report'):   
                #     request.session.flush()
                #     messages.success(request, "Sesi anda sudah habis, silahkan Login kembali.")
                #     return HttpResponseRedirect(reverse('bimbel_app:login'))
                # else:
                #     request.session['last_login_timestamp'] = now        
                #     return response

                if(request.session.get('username_final')):
                    menus = ['/dash/','/dash/logout/']

                    if(request.path in ['/dash/login/']):
                        return HttpResponseRedirect(reverse('bimbel_app:index'))     
                return response
    return middleware
 

