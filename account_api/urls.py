from django.urls import path
from . import views


urlpatterns = [
    path('api/post/', views.PostListView.as_view()), # All Posts
    path('api/account/', views.UsersView.as_view()), # All Auth Users
    path('api/post_add/', views.PostAddView.as_view()), # Post Add
    path('api/post/<int:id>/edit/', views.PostDeleteUpdateView.as_view()), # Edit Post (Delete, Update)
    path('api/post/<int:id>/', views.PostRetrieveView.as_view()), # Detail Post
    path('api/post/<int:post_id>/comment_add/', views.CommentAddView.as_view()), # Add Comment
    path('api/comment/<int:id>/edit/', views.CommentDeleteUpdateView.as_view()), # Edit Comment (Delete, Update)
    path('api/post/<int:post_id>/comment/', views.CommectListView.as_view()), # All Comments from Post
    path('api/post/<int:post_id>/mark_add/', views.RatingAddView.as_view()), # Add Rate to Post
    path('api/mark/<int:id>/edit/', views.RatingDeleteUpdateView.as_view()) # Edit Rate (Delete, Update)

]


