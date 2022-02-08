from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

import authentication.views
import blog.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication.views.login_page, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('flux/', blog.views.flux, name='flux'),
    path('subscriptions/', blog.views.subscriptions, name='subscriptions'),
    path('unsubscribe/<user_follows_id>', blog.views.unsubscribe, name='unsubscribe'),
    path('ticket_creation/', blog.views.ticket_creation, name='ticket_creation'),
    path('review_creation/', blog.views.review_creation, name='review_creation'),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
