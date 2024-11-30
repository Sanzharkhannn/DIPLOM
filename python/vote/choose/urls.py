from django.urls import path
from . import views
app_name = 'choose'

urlpatterns = [
# представления поста
    path('', views.index, name='index'),
    path('register/', views.user_register, name='user-register'),
    path('login/', views.user_login, name='user-login'),
    path('logout/', views.user_logout, name='user-logout'),
    path('logined-page/', views.logined_page, name='logined-page'),
    path('vote/', views.vote_page, name='vote-page'),
    path('vote/create', views.create_content, name='create-content'),
    path('vote-success/', views.vote_success, name='vote-success'),  # Опционально
    path('vote/user/createvote', views.show_votes, name='vote-page'),
]