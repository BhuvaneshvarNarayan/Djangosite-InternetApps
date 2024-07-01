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
    ]
