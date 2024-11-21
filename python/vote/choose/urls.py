from django.urls import path
from . import views
app_name = 'choose'

urlpatterns = [
# представления поста
#    path('', views.option_list, name='option_list'),
 #   path('<int:option_id>', views.vote, name='vote'),
    path('choose/', views.chooses, name='chooses'),
]