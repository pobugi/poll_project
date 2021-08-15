from django.shortcuts import get_object_or_404, render
from rest_framework import views, viewsets, permissions, mixins
from .models import Poll, Question, Answer, AnswerOption
from .serializers import (
    PollSerializer, 
    QuestionSerializer, 
    AnswerSerializer, 
    AnswerOptionSerializer,
    AnswerCustomTextSerializer,
    AnswerSingleOptionSerializer, 
    AnswerMultipleOptionSerializer,
    UserPollSerializer
)
from datetime import datetime as dt
from django.db.models import Q, query

class PollView(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (permissions.IsAdminUser, )

class ActivePollView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Poll.objects.filter(end_date__gte=dt.today())
    serializer_class = PollSerializer


class QuestionView(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAdminUser, )


    def get_queryset(self):
        poll = get_object_or_404(Poll, id=self.kwargs['id'])
        return poll.questions.all()

    def perform_create(self, serializer):
        poll = get_object_or_404(Poll, pk=self.kwargs['id'])
        serializer.save(poll=poll)


class AnswerView(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class AnswerCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_serializer_class(self):
        question = get_object_or_404(
            Question, 
            pk=self.kwargs['question_pk'],
            poll__id=self.kwargs['id']
        )

        if question.type == 'text':
            return AnswerCustomTextSerializer
        elif question.type == 'radio':
            return AnswerSingleOptionSerializer
        elif question.type == 'checkbox':
            return AnswerMultipleOptionSerializer

    def perform_create(self, serializer):
        question = get_object_or_404(
            Question, 
            pk=self.kwargs['question_pk'],
            poll__id=self.kwargs['id']
        )
        serializer.save(person=self.request.user, question=question)

class AnswerOptionView(viewsets.ModelViewSet):
    queryset = AnswerOption.objects.all()
    serializer_class = AnswerOptionSerializer
    permission_classes = (permissions.IsAdminUser,)

    def perform_create(self, serializer):
        question = get_object_or_404(
            Question,
            pk=self.kwargs['question_pk'],
            poll__id=self.kwargs['id']
        )
        serializer.save(question=question)
    
    def get_queryset(self):
        question=get_object_or_404(Question, id=self.kwargs['question_pk'])
        return question.answer_options.all()


class UserIdPollListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UserPollSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Poll.objects.exclude(
            ~Q(questions__answers__person__id=user_id)
        )
        return queryset