from django.urls import path
from . import views
urlpatterns = [
	path('', views.index),
	path('create_user', views.create_user),
	path('login', views.login), 	
	path('success', views.success),
	path('logout', views.logout)
]