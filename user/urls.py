from django.urls import path
from .views import UserCreate, UserNotesListView
urlpatterns = [
    path('user/', UserCreate.as_view()),
    path('user/auth/', UserCreate.as_view()),
    path('user/sites/', UserNotesListView.as_view())
]