from django.conf.urls import url 
 
from . import views 

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^signin$', views.signin, name = 'signin'),
    url(r't$', views.t, name='t')
]