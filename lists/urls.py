from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('create_list/', views.create_list, name="create_list"),
    path('delete_list/<int:list_id>', views.delete_list, name="delete_list"),
    path('create_item/<int:list_id>', views.create_item, name="create_item"),
    path('get_items/<int:list_id>', views.get_items, name="get_items"),
    path('delete_item/<int:item_id>', views.delete_item, name="delete_item"),
    path('approve_item/<int:item_id>', views.approve_item, name="approve_item"),
]
