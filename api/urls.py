from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('api/summarize/', views.generate_summary, name='summarize'),
]