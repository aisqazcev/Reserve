from django.urls import path
from .views import PostListView, PostShowView

app_name="reserve"

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<slug:post_slug>/', PostShowView.as_view(), name='post-show'),
]