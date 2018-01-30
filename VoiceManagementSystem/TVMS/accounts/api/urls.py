from django.contrib import admin
from django.conf.urls import url
from .views import UserLoginAPIView
app_name = 'accounts'
urlpatterns = [
    url(r'login/$', UserLoginAPIView.as_view(), name = 'login'),
    #url(r'logout/$', auth_view.LogoutView.as_view(), name='logout'),
]
