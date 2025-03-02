from django.urls import path
from . import views
from .views import start_parsing_view, stop_task_view, book_fin

urlpatterns = [
    path('book/', views.BookListView.as_view(), name='book_list'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('book/<int:pk>/', start_parsing_view, name='parse_view'),
    path('book/<int:pk>/delete/', views.BookDeliteView.as_view(), name='book_delete'),
    path('stop-task/', stop_task_view, name='stop_task'),
    path('book-find/', book_fin, name='book_find'),
    path('chapter/<int:pk>/', views.ChapterDetailView.as_view(), name='chapter_detail'),
    path('chapter/<int:pk>/delete/', views.ChapterDeleteView.as_view(), name='chapter_delete'),
]
