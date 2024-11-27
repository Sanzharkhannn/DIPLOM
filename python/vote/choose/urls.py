from django.urls import path
from . import views
app_name = 'choose'

urlpatterns = [
# представления поста
    path('', views.index, name='index'),
    path('lists/', views.option_list, name='list of options'),
    path('lists/create', views.create_option, name='create option')
    #path('choose/', views.chooses, name='chooses'),
   # path('create/', views.create_poll, name='create_poll'),
]