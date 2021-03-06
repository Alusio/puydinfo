from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('calendrier', views.calendar, name='calendar'),
    path('period/<slug:slug>', views.period, name='period'),
    path('', views.index_temp),
    path('show/<slug:slug>', views.shows, name="show"),
    path('animation/<slug:slug>', views.animation, name="animation"),
    path('ville/<slug:slug>', views.ville, name="ville"),
    path('restaurant/<slug:slug>', views.restaurant, name='restaurant'),
    path('hotel/<slug:slug>', views.hotel, name='hotel'),
    path('planner', views.parametres),
    path('programme', views.resultat),
    path('mentions_legales', views.legales),
    path('signup/', views.SignUp, name='signup'),
    path('update/', views.update_profile, name='update'),
    path('profile/', views.profile, name='profile'),
    path('groupe/', views.group, name='group'),
    path('groupe/edit', views.group_edit, name='group_edit'),
    path('member/add/<int:pk>', views.member_add, name='member_add'),
    path('member/edit/<int:pk>', views.member_edit, name='member_edit'),
    path('member/delete/<int:pk>', views.member_delete, name='member_delete'),
    path('result', views.programmation, name='programation'),
    path('result_live', views.resultat_live, name='result_live'),
    path('api/<str:id>', views.api, name='api'),
    path('getdata', views.getdata, name='getdata'),
    path('index_off', views.index_off, name='index_off'),
    path('article/<slug:slug>', views.articles, name='articles'),
    path('sejour/', views.sejour, name='sejour'),
    path('sejour/add', views.sejour_add, name='sejour_add'),
    path('sejour/edit/<int:pk>', views.sejour_edit, name='sejour_edit'),
    path('sejour/delete/<int:pk>', views.sejour_delete, name='sejour_delete'),
    path('upload_picture', views.upload_picture, name='upload_picture'),
    path('planner_perso', views.prog_perso, name='prog_perso'),
]

