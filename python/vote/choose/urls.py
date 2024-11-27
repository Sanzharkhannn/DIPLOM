from django.urls import path
from . import views
app_name = 'choose'

urlpatterns = [
# представления поста
    path('', views.index, name='index'),
]