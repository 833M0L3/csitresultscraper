from django.contrib import admin
from django.urls import path, include
from result import views


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('admin/', admin.site.urls),
    path('result/', include('result.urls', namespace='result')),
]