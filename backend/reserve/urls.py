from django.urls import path
from .views import PostListView, PostShowView

app_name="reserve"

urlpatterns = [
    path('posts/', PostListView.as_view()),
    path('posts/<post_slug>/', PostShowView.as_view()),
]