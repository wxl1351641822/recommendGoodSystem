from app import sql
from django.shortcuts import HttpResponse,render,redirect
import traceback
import json
import time

def start(request):#函数用于
    return render(request, 'start.html')


def layout(request):#函数用于
    return render(request, 'layout.html')


def good(request):#函数用于
    return render(request, 'good/good_exlayout.html')

def user(request):#函数用于
    return render(request, 'user/user_exlayout.html')












