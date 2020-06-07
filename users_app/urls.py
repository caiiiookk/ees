from django.urls import path, include
from .views import (
    users_view,
    profile_view,
    my_profile_view,
    login_view,
    sign_up_view,
    logout_view,
    ProfileEditView,
    ProfileAdminPanelView,
    change_password_view,
)

app_name = 'users_app'

urlpatterns = [
    path('', users_view, name='users'),
    path('<int:id>/', profile_view, name='profile'),
    path('<int:id>/edit/', ProfileEditView.as_view(), name='edit'),
    path('<int:id>/admin-panel/', ProfileAdminPanelView.as_view(), name='admin-panel'),
    path('my/', my_profile_view, name='my_profile'),
    path('login/', login_view, name='login'),
    path('sign_up/', sign_up_view, name='sign_up'),
    path('logout/', logout_view, name='logout'),
    path('change_password/', change_password_view, name='pw_change')
]
