from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register('polls', views.PollView)
# router.register('active_polls', views.ActivePollView)
# router.register('questions', views.QuestionView)
# router.register('answers', views.AnswerView)
# router.register('answer_options', views.AnswerOptionView)

router.register(
    'polls/(?P<id>\d+)/questions',
    views.QuestionView,
    basename='questions'
)

router.register(
    'polls/(?P<id>\d+)/questions/(?P<question_pk>\d+)/answer_options',
    views.AnswerOptionView,
    basename='answer_options'
)

router.register('active_polls', views.ActivePollView)

router.register(
    'polls/(?P<id>\d+)/questions/(?P<question_pk>\d+)/answers',
    views.AnswerCreateViewSet,
    basename='answers'
)

router.register(
    'my_polls',
    views.UserIdPollListView,
    basename='userid_polls'
)

urlpatterns = [
    path('', include(router.urls)),
]