from django.shortcuts import render
from django.db.models import Sum
from django.http import JsonResponse,HttpResponse,HttpResponseNotFound
import json,sys

from .models import *


# Create your views here.

def users(request):
    users = request.GET.get('users')
    if users:
        users = json.loads(users.replace('\'','"'))
        user_objects = [get_user_object(user.id) for user in User.objects.filter(name__in = users)]
    else:
        user_objects = [get_user_object(user.id) for user in User.objects.all()]
    return JsonResponse({'users':user_objects}, safe=False)

def add(request):
    user = request.POST.get('user')
    if user:
        user_object = {'name':user}
        user_object['owes'] = dict((user.name,0) for user in User.objects.all())
        user_object['owed_by'] = dict((user.name,0) for user in User.objects.all())
        user_object['balance'] = 0
        User.objects.create(name=user)
        return JsonResponse(user_object, safe=False)
    else:
        return HttpResponse(status=200)

def get_user_object(user_id):
    user = User.objects.get(id=user_id)
    user_object = {'name':user.name}
    owes = {}
    owed_by = {}
    for user in User.objects.exclude(id=user_id).order_by('name'):
        owes[user.name] = Transaction.objects.filter(borrower=user_id,lender=user.id).aggregate(owed_amount=Sum('amount'))['owed_amount'] if Transaction.objects.filter(borrower=user_id,lender=user.id).exists() else 0
        owed_by[user.name] = Transaction.objects.filter(borrower=user.id,lender=user_id).aggregate(owes_amount=Sum('amount'))['owes_amount'] if Transaction.objects.filter(borrower=user.id,lender=user_id).exists()  else 0
    
    user_object['owes'] = owes
    user_object['owed_by'] = owed_by
    owed_total = Transaction.objects.filter(lender=user_id).aggregate(owed_balance=Sum('amount'))['owed_balance'] if Transaction.objects.filter(lender=user_id).exists() else 0
    owes_total = Transaction.objects.filter(borrower=user_id).aggregate(owes_balance=Sum('amount'))['owes_balance'] if Transaction.objects.filter(borrower=user_id).exists() else 0
    user_object['balance'] = owed_total-owes_total
    return user_object

def iou(request):
    lender = request.POST.get('lender')
    borrower = request.POST.get('borrower')
    amount = request.POST.get('amount')
    if lender and borrower and amount:
        lender_id = User.objects.get(name=lender).id
        borrower_id = User.objects.get(name=borrower).id
        Transaction.objects.create(borrower=borrower_id,lender=lender_id,amount=amount)
        users = [lender,borrower]
        user_objects = [get_user_object(user.id) for user in User.objects.filter(name__in = users)]
        return JsonResponse({users:user_objects}, safe=False)
    else:
        return HttpResponse(status=200)