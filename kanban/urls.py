from django.urls import include, path
from kanban import views

app_name = 'kanban'

urlpatterns = [
    path('users/', include('users.urls')),
    path('auth/', include('rest_auth.urls')),
    path('auth/registration/', include('rest_auth.registration.urls')),
    path('trello-users/', views.TrelloUserView.as_view()),
    path('boards/', views.BoardView.as_view()),
    path('board-members/', views.BoardMemberView.as_view()),
    path('lists/', views.ListView.as_view()),
    path('cards/', views.CardView.as_view()),
    path('card/<int:pk>', views.CardDetailView.as_view()),
    path('attachments/', views.AttachmentView.as_view()),
]
