from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from ..decorators import foodriver_required
from ..forms import FoodriverRequirementsForm, FoodriverSignUpForm
from ..models import Pickup, Foodriver, TakenPickup, User


class FoodriverSignUpView(CreateView):
    model = User
    form_class = FoodriverSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'foodriver'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('foodrivers:pickup_list')


@method_decorator([login_required, foodriver_required], name='dispatch')
class FoodriverInterestsView(UpdateView):
    model = Foodriver
    form_class = FoodriverRequirementsForm
    template_name = 'classroom/students/interests_form.html'
    success_url = reverse_lazy('foodrivers:pickup_list')

    def get_object(self):
        return self.request.user.foodriver

    def form_valid(self, form):
        messages.success(self.request, 'Requirements updated with success!')
        return super().form_valid(form)


@method_decorator([login_required, foodriver_required], name='dispatch')
class PickupListView(ListView):
    model = Pickup
    ordering = ('name', )
    context_object_name = 'pickups'
    template_name = 'classroom/students/quiz_list.html'  #pickup_list.html

    def get_queryset(self):
        foodriver = self.request.user.foodriver
        foodriver_interests = foodriver.interests.values_list('pk', flat=True)
        taken_pickups = foodriver.pickups.values_list('pk', flat=True)
        queryset = Pickup.objects.filter(area__in=foodriver_interests) \
            .exclude(pk__in=taken_pickups) \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)
        return queryset


@method_decorator([login_required, foodriver_required], name='dispatch')
class TakenPickupListView(ListView):
    model = TakenPickup
    context_object_name = 'taken_pickups'
    template_name = 'classroom/students/taken_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.foodriver.taken_pickups \
            .select_related('pickup', 'pickup__area') \
            .order_by('pickup__name')
        return queryset



######### 4 george #########

# @login_required
# @student_required
# def take_quiz(request, pk):
#     quiz = get_object_or_404(Quiz, pk=pk)
#     student = request.user.student

#     if student.quizzes.filter(pk=pk).exists():
#         return render(request, 'students/taken_quiz.html')

#     total_questions = quiz.questions.count()
#     unanswered_questions = student.get_unanswered_questions(quiz)
#     total_unanswered_questions = unanswered_questions.count()
#     progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
#     question = unanswered_questions.first()

#     if request.method == 'POST':
#         form = TakeQuizForm(question=question, data=request.POST)
#         if form.is_valid():
#             with transaction.atomic():
#                 student_answer = form.save(commit=False)
#                 student_answer.student = student
#                 student_answer.save()
#                 if student.get_unanswered_questions(quiz).exists():
#                     return redirect('students:take_quiz', pk)
#                 else:
#                     correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
#                     score = round((correct_answers / total_questions) * 100.0, 2)
#                     TakenQuiz.objects.create(student=student, quiz=quiz, score=score)
#                     if score < 50.0:
#                         messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s.' % (quiz.name, score))
#                     else:
#                         messages.success(request, 'Congratulations! You completed the quiz %s with success! You scored %s points.' % (quiz.name, score))
#                     return redirect('students:quiz_list')
#     else:
#         form = TakeQuizForm(question=question)

#     return render(request, 'classroom/students/take_quiz_form.html', {
#         'quiz': quiz,
#         'question': question,
#         'form': form,
#         'progress': progress
#     })
