from django.contrib import admin
from django.contrib.auth.views import (
    LogoutView, PasswordResetView, PasswordResetDoneView)
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

import authentication.views
import blog.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication.views.login_page, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset-password/', PasswordResetView.as_view(
        template_name='authentication/password_reset_form.html'),
         name='password_reset'
         ),
    path('reset-password-done/', PasswordResetDoneView.as_view(
        template_name='authentication/password_reset_done.html'),
         name='password_reset_done'
         ),
    path('signup/', authentication.views.signup, name='signup'),
    path('home/', blog.views.home, name='home'),
    path('subscriptions/', blog.views.subscriptions, name='subscriptions'),
    path('unsubscribe/<user_follows_id>', blog.views.unsubscribe, name='unsubscribe'),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
