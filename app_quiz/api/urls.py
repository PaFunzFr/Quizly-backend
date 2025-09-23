from django.urls import path
from .views import QuizCreateView

urlpatterns = [
    path('', QuizCreateView.as_view(), name='create-quiz')
    # path('<int:pk>/', QuizDetailView.as_view(), name="quiz-detail")
]
