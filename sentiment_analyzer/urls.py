from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('amazon', views.amazon_review, name='amazon'),
    path('single', views.sentiment_check, name='single'),
    path('features', views.features, name='features'),
]