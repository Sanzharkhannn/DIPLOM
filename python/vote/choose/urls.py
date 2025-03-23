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
    path('user/id', views.userPage, name='user-page'),
    path('world', views.worldPage, name='world-page'),

    path('create-club-vote/', views.create_club_vote, name='create-club-vote'),
    path('create-player-vote/', views.create_player_vote, name='create-player-vote'),
    path('create-movie-vote/', views.create_movie_vote, name='create-movie-vote'),
    path('create-actor-vote/', views.create_actor_vote, name='create-actor-vote'),
    path('create-profession-vote/', views.create_profession_vote, name='create-profession-vote'),
    path('create-famous-vote/', views.create_famous_vote, name='create-famous-vote'),
]