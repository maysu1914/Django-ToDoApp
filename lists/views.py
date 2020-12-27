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

today = datetime.date.today()


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
            if stock.status == 'Not Completed' and stock.deadline < today:
                stock.status = 'Expired'
            elif stock.status == 'Expired' and stock.deadline >= today:
                stock.status = 'Not Completed'
            else:
                pass
            stock.list_id = List.objects.get(id=list_id)
            stock.save()
        else:
            errors_data = {}
            for field in form:
                errors = []
                for error in field.errors:
                    errors.append(error)
                errors_data[field.name] = errors
            response_data = {'errors': errors_data}
            # print(response_data)

            return JsonResponse(response_data, status=500)
    return redirect('home')


@login_required(login_url='login')
def get_items(request, list_id):
    queries = {'status': ['Not Completed', 'Completed', 'Expired']}
    orders = {'sort': ['deadline', 'name', 'created']}
    response_data = {'result': 'error', 'message': ''}
    update_status(request)
    if request.method == 'GET':
        user_check = List.objects.filter(user_id=request.user, id=list_id)
        if user_check:
            filters = {}
            sorting = []
            for query in request.GET:
                if query in queries and request.GET[query] in queries[query]:
                    filters[query] = request.GET[query]
                elif query in orders and request.GET[query] in orders[query]:
                    sorting.append(request.GET[query])
            result = Item.objects.filter(list_id=list_id, **filters).order_by(*sorting)
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
    Item.objects.filter(status="Not Completed", deadline__lt=today).update(status='Expired')
    # Item.objects.filter(status="Expired", deadline__gt=today).update(status='Not Completed')
