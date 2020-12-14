import datetime

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q

import json

# Create your views here.
from lists.forms import CreateListForm, CreateItemForm
from lists.models import List, Item


@login_required(login_url='login')
def home(request):
    new_item_form = CreateItemForm()
    lists = List.objects.order_by('-created_at').filter(user_id=request.user)
    items = Item.objects.filter(list_id=lists)
    context = {'lists': lists, 'items': items, 'new_item_form': new_item_form}
    return render(request, 'lists/home.html', context)


@login_required(login_url='login')
def create_list(request):
    if request.method == 'POST':
        form = CreateListForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.user_id = request.user
            stock.save()
    return redirect('home')


@login_required(login_url='login')
def create_item(request, list_id):
    if request.method == 'POST':
        form = CreateItemForm(request.POST)
        user_check = List.objects.filter(user_id=request.user, id=list_id)
        if form.is_valid() and user_check:
            stock = form.save(commit=False)
            stock.list_id = List.objects.get(id=list_id)
            stock.save()
    return redirect('home')


@login_required(login_url='login')
def get_items(request, list_id):
    update_status(request)
    if request.method == 'GET':
        queries = {'status': ['Not Completed', 'Completed', 'Expired'], 'sort': ['deadline', 'name', 'created']}
        response_data = {'result': 'error', 'message': ''}
        user_check = List.objects.filter(user_id=request.user, id=list_id)
        if user_check:
            result = Item.objects.filter(list_id=list_id);
            for query in request.GET:
                if request.GET[query] in queries['status']:
                    result = result.filter(status=request.GET[query])
                if request.GET[query] in queries['sort']:
                    result = result.order_by(request.GET[query])

            response_data['result'] = serializers.serialize('json', result)
            response_data['message'] = 'Success'
            return JsonResponse(response_data)
        else:
            response_data['message'] = "You don't have access to this area."
            return JsonResponse(response_data)
    return redirect('home')


@login_required(login_url='login')
def delete_item(request, item_id):
    if request.method == 'GET':
        item = Item.objects.get(id=item_id)
        user_check = List.objects.filter(user_id=request.user, id=item.list_id.id)
        if user_check:
            Item.objects.get(id=item_id).delete()
    return redirect('home')


@login_required(login_url='login')
def delete_list(request, list_id):
    if request.method == 'GET':
        response_data = {'result': 'error', 'message': ''}
        user_check = List.objects.filter(user_id=request.user, id=list_id)
        if user_check:
            response_data['result'] = List.objects.get(id=list_id).delete()
            response_data['message'] = 'Success'

        else:
            response_data['message'] = "You don't have access to this area."
            return JsonResponse(response_data)
    return redirect('home')


@login_required(login_url='login')
def approve_item(request, item_id):
    if request.method == 'GET':
        response_data = {'result': 'error', 'message': ''}
        item = Item.objects.get(id=item_id)
        user_check = List.objects.filter(user_id=request.user, id=item.list_id.id)
        if user_check:
            response_data['result'] = Item.objects.filter(id=item_id).update(status='Completed')
            response_data['message'] = 'Success'
            return JsonResponse(response_data)
        else:
            response_data['message'] = "You don't have access to this area."
            return JsonResponse(response_data)
    return redirect('home')


@login_required(login_url='login')
def update_status(request):
    today = datetime.date.today()
    result = Item.objects.filter(~Q(status="Completed"), deadline__lte=today).update(status='Expired')
