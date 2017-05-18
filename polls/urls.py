from django.conf.urls import url 
 
from . import views 

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^signin$', views.signin, name = 'signin'),
    url(r'^recommend$', views.recommend, name='recommend'),
    url(r'^search/', views.search, name = 'search'),
    url(r'^signout$', views.signout, name = 'signout'),
    url(r'^single/', views.single, name = 'single')
]
