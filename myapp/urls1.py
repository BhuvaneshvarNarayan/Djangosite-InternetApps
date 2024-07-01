from django.urls import path, re_path
from myapp import views1

app_name = 'myapp'

urlpatterns = [
    path(r'', views1.index, name='index'),
    path('', views1.publisher(), name = 'publisher'),
    re_path(r'^(?P<book_id>\d+)/$', views1.detail, name='detail'),
]
