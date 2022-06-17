from django.urls import path
from django.views.decorators.cache import cache_page

from sofia_weather import views

urlpatterns = [
    path('', cache_page(60*60)(views.IndexView.as_view()), name='index'),
    path('subscribe/', views.SubscribeUserView.as_view(), name='subscribe'),
]