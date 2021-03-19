from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import UserSignUpView, UserLoginView, UserLogoutView

app_name = 'authentication'

urlpatterns = [
    path(
        'signup/',
        UserSignUpView.as_view(),
        name='signup'
    ),
    path(
        'login/',
        UserLoginView.as_view(
            template_name='login.html'
        ),
        name='login'
    ),
    path(
        'logout/',
        UserLogoutView.as_view(),
        name='logout'
    ),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            success_url='done'
        ),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html",
            success_url='done'
        ),
        name='password_reset_confirm'

    ),
    path(
        'reset/<uidb64>/set-password/done',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]
