from django.conf.urls import url

from user import views

urlpatterns = [
    url(r'^login$', views.UserLogin, name='login'),
    url(r'^logout$', views.UserLogout, name='logout')
]
