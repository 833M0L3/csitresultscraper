from django.urls import path
from . import views
app_name = 'result'

urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    path('<str:id>/', views.post_detail, name='post_detail'),
]