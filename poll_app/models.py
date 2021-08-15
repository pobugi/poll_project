from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime


User = get_user_model()


class Poll(models.Model):
    name = models.CharField(max_length=30)
    start_date = models.DateField(auto_now_add=True) # start_date = date of poll creation, cannot be changed
    end_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.name


QUESTION_TYPES = (
    ('text', 'Text'),
    ('radio', 'One option'),
    ('checkbox', 'Multiple options'),
)

class Question(models.Model):
    text = models.TextField(verbose_name="Text of a new question")
    type = models.CharField(
        max_length=30, 
        choices=QUESTION_TYPES, 
        )
    poll = models.ForeignKey(
        Poll, 
        blank=True,
        on_delete=models.CASCADE,
        related_name="questions")

    def __str__(self):
        return self.text 


class AnswerOption(models.Model):
    option = models.TextField(verbose_name='Possible answer option')
    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE, 
        related_name='answer_options')

    def __str__(self):
        return self.option 


class Answer(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

    multiple_answer = models.ManyToManyField(AnswerOption)
    single_answer = models.ForeignKey(
        AnswerOption, 
        on_delete=models.CASCADE, 
        null=True,
        related_name='answers_single_answer')
    text_answer = models.TextField(null=True)
    
    # def __str__(self):
    #     return self.person.name + "'s answer" 
