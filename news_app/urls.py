from django.urls import path
from .views import (
    NewsView,
    NewsAddView,
    NewsEditView,
    NewsShowView,
    NewsDeleteView,
)

app_name = 'news_app'

urlpatterns = [
    path('', NewsView.as_view(), name='news'),
    path('<int:id>/edit/', NewsEditView.as_view(), name='edit'),
    path('<int:id>/edit/delete/', NewsDeleteView.as_view(), name='delete'),
    path('add/', NewsAddView.as_view(), name='add'),
    path('<int:id>/', NewsShowView.as_view(), name='show'),
]
