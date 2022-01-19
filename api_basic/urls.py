from django.urls import path
from .views import ArticleAPIView,ArticleDetails,GenericAPIView

urlpatterns = [
    # path('article/', article_list),
    path('articleapi/', ArticleAPIView.as_view()),
    path('articleapi/<int:id>/', ArticleDetails.as_view()),
    path('articlegeneric/<int:id>', GenericAPIView.as_view()),
    # path('article/<int:pk>/', article_detail),
]
