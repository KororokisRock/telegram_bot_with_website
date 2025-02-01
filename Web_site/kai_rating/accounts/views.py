from django.shortcuts import render
from django.http import HttpResponse

from . import db





# Create your views here.


def login(request):
    return render(request, 'accounts/login.html')


def reg(request):
    
    if request.method == 'POST':
        req = request.POST
        if req['password']==req['confirm-password'] and db.is_valid_password(req['password']):
            is_same=True
            is_hard = True
            db.user_to_db(req['username'],req['password'])
            return HttpResponse('регистрация север')
        elif req['password']!=req['confirm-password'] and db.is_valid_password(req['password']):
            is_hard = True
            is_same = False
            context={
                'flag_1':is_same,
                'flag_2':is_hard
            }
            return render(request, 'accounts/registr.html',context)
        elif req['password']==req['confirm-password'] and not db.is_valid_password(req['password']):
            is_same=True
            is_hard = False
            context={
                'flag_1':is_same,
                'flag_2':is_hard
            }
            return render(request, 'accounts/registr.html',context)
        else:
            is_same=False
            is_hard = False
            context={
                'flag_1':is_same,
                'flag_2':is_hard
            }
            return render(request, 'accounts/registr.html',context)
    else:
        return render(request, 'accounts/registr.html')


        
        
    