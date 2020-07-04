from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib import admin
from django.db import models
from django.utils.html import escape, mark_safe
from datetime import datetime


class User(AbstractUser):
    is_foodriver = models.BooleanField(default=False)
    is_foodonator = models.BooleanField(default=False)
    is_shelter = models.BooleanField(default=False)


class Area(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)
    

class Pickup(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pickups')
    cuisine = models.CharField(max_length=255)
    quantity = models.IntegerField()
    best_by = models.DateTimeField(default=datetime.now(),blank=True)
    created = models.DateTimeField(auto_now_add=True,
                                help_text="The date and time this pickup was created. Automatically generated when the model saves.")
    modified = models.DateTimeField(auto_now=True,
                                help_text="The date and time this pickup was updated. Automatically generated when the model updates.")
    image = models.ImageField(default='default.jpg', upload_to='donation_pics')

    def __str__(self):
        return self.cuisine

# class Question(models.Model):
#     quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
#     text = models.CharField('Question', max_length=255)

#     def __str__(self):
#         return self.text


class Foodriver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    pickups = models.ManyToManyField(Pickup, through='TakenPickup')
    requirements = models.ManyToManyField(Area, related_name='interested_foodrivers')

    # def get_unanswered_questions(self, quiz):
    #     answered_questions = self.quiz_answers \
    #         .filter(answer__question__quiz=quiz) \
    #         .values_list('answer__question__pk', flat=True)
    #     questions = quiz.questions.exclude(pk__in=answered_questions).order_by('text')
    #     return questions

    def __str__(self):
        return self.user.username


class TakenPickup(models.Model):
    foodriver = models.ForeignKey(Foodriver, on_delete=models.CASCADE, related_name='taken_pickups')
    pickup = models.ForeignKey(Pickup, on_delete=models.CASCADE, related_name='taken_pickups')
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


# class StudentAnswer(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_answers')
#     answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')
