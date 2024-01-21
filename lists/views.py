from django.shortcuts import redirect, render
from lists.models import Item


def home_page(request):
    '''домашняя страница'''
    return render(request, 'home.html')


def view_list(request):
    '''представление списка'''
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})


def new_list(request):
    '''новый список'''
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/the-one-of-a-kind-list-in-the-world/')
