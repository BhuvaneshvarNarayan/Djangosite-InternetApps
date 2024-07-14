from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
    path(r'', views.index, name='index'),
    #path(r'', views.about, name='about'),
    path('about/', views.about, name='about'),
    path('<int:book_id>/', views.detail_view, name='detail'),
    path('feedback/', views.getFeedback, name='feedback'),
    path('findbooks/', views.findbooks, name='findbooks'),
    path('place_order/', views.place_order, name='place_order'),
    path('review/', views.review, name='review'),
    path('chk_reviews/<int:book_id>/', views.chk_reviews, name='chk_reviews'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    ]
