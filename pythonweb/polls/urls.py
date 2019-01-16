from django.urls import path
from .views import index, detail, result

urlpatterns = [
    path('', index, name='index'),
    path('<int:question_id>/', detail, name='detail'),
    path('<int:question_id>/result/', result, name='result'),
]