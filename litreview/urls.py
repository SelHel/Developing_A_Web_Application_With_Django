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
    path('posts/', blog.views.posts, name='posts'),
    path('subscriptions/', blog.views.subscriptions, name='subscriptions'),
    path('unsubscribe/<user_follows_id>', blog.views.unsubscribe, name='unsubscribe'),
    path('ticket_creation/', blog.views.ticket_creation, name='ticket_creation'),
    path('ticket_modification/<ticket_id>', blog.views.ticket_modification, name='ticket_modification'),
    path('ticket_deletion/<ticket_id>', blog.views.ticket_deletion, name='ticket_deletion'),
    path('ticket_confirm_deletion/<ticket_id>', blog.views.ticket_confirm_deletion, name='ticket_confirm_deletion'),
    path('ticket_review_creation/<ticket_id>', blog.views.ticket_review_creation, name='ticket_review_creation'),
    path('review_creation/', blog.views.review_creation, name='review_creation'),
    path('review_modification/<review_id>', blog.views.review_modification, name='review_modification'),
    path('review_deletion/<review_id>', blog.views.review_deletion, name='review_deletion'),
    path('review_confirm_deletion/<review_id>', blog.views.review_confirm_deletion, name='review_confirm_deletion'),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
