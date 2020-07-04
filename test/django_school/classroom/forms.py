from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django import forms
from phone_field import PhoneField
from django.forms.utils import ValidationError
from django.shortcuts import render, redirect
from classroom.models import (Foodriver, Area, User, Pickup)


class FoodonatorSignUpForm(UserCreationForm):
    restaurant_name = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=150)
    phone = forms.CharField(max_length=150, help_text='Contact phone number')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('restaurant_name', 'email', 'phone')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_foodonator = True
        if commit:
            user.save()
        return user


class FoodriverSignUpForm(UserCreationForm):
    foodriver_name = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=150)
    phone = forms.CharField(max_length=150, help_text='Contact phone number')
    requirements = forms.ModelMultipleChoiceField(
        queryset=Area.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        help_text=('Don\'t worry if you don\'t have all of these yet, we will work with you to help you satisfy these requirements.')
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('foodriver_name', 'email', 'phone', 'requirements')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_foodriver = True
        user.save()
        foodriver = Foodriver.objects.create(user=user)
        foodriver.requirements.add(*self.cleaned_data.get('requirements'))
        return user


class FoodriverRequirementsForm(forms.ModelForm):
    class Meta:
        model = Foodriver
        fields = ('requirements', )
        widgets = {
            'requirements': forms.CheckboxSelectMultiple
        }


# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = ('text', )


# class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
#     def clean(self):
#         super().clean()

#         has_one_correct_answer = False
#         for form in self.forms:
#             if not form.cleaned_data.get('DELETE', False):
#                 if form.cleaned_data.get('is_correct', False):
#                     has_one_correct_answer = True
#                     break
#         if not has_one_correct_answer:
#             raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')


# class TakePickupForm(forms.ModelForm):
#     answer = forms.ModelChoiceField(
#         queryset=Answer.objects.none(),
#         widget=forms.RadioSelect(),
#         required=True,
#         empty_label=None)

#     class Meta:
#         model = StudentAnswer
#         fields = ('answer', )

#     def __init__(self, *args, **kwargs):
#         question = kwargs.pop('question')
#         super().__init__(*args, **kwargs)
#         self.fields['answer'].queryset = question.answers.order_by('text')
