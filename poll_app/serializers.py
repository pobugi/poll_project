from django.db import models
from rest_framework import serializers
from rest_framework.utils import field_mapping
from django.db.models import Q, fields, query
from .models import Poll, Question, Answer, AnswerOption


class PollSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poll
        fields = (
            'id', 'name', 'end_date', 'description'
        )

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        # fields = ('id', 'person_id')
        fields = '__all__'

class AnswerOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnswerOption
        fields = '__all__'


class UserFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        question_id = self.context.get('request').parser_context['kwargs'][
            'question_pk']
        request = self.context.get('request', None)
        queryset = super(UserFilteredPrimaryKeyRelatedField,
                         self).get_queryset()
        if not request or not queryset:
            return None
        return queryset.filter(question_id=question_id)


class AnswerCustomTextSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('text_answer', )
        model = Answer


class AnswerSingleOptionSerializer(serializers.ModelSerializer):
    single_option = UserFilteredPrimaryKeyRelatedField(
        many=False,
        queryset=AnswerOption.objects.all()
    )

    class Meta:
        fields = ('single_option', )
        model = Answer


class AnswerMultipleOptionSerializer(serializers.ModelSerializer):
    multiple_answer = UserFilteredPrimaryKeyRelatedField(
        many=True,
        queryset=AnswerOption.objects.all()
    )

    class Meta:
        fields = ('multiple_answer',)
        # fields = '__all__'
        model = Answer


class QuestionListSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField('get_answers')

    class Meta:
        fields = '__all__'
        model = Question

    def get_answers(self, question):
        person_id = self.context.get('request').user.id
        answers = Answer.objects.filter(
            Q(question=question) & Q(person__id=person_id)
        )
        serializer = AnswerSerializer(instance=answers, many=True)
        return serializer.data


class UserPollSerializer(serializers.ModelSerializer):
    questions = QuestionListSerializer(read_only=True, many=True)

    class Meta:
        fields = '__all__'
        model = Poll
