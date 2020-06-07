from django.urls import path, include
from .views import (
    MainView,
    AboutView,
    ContactsView,
    EditPageView,
)

app_name = 'main_app'

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('about/', AboutView.as_view(), name='about'),
    path('<str:name>/edit/', EditPageView.as_view(), name='edit'),
]
