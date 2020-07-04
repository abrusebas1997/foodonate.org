from django.urls import include, path

from .views import classroom, foodrivers, foodonators

urlpatterns = [
    path('', classroom.home, name='home'),

    path('foodrivers/', include(([
        path('', foodrivers.PickupListView.as_view(), name='pickup_list'),
        path('interests/', foodrivers.FoodriverInterestsView.as_view(), name='foodriver_interests'),
        path('taken/', foodrivers.TakenPickupListView.as_view(), name='taken_pickup_list'),  # foodrivers
        # path('pickup/<int:pk>/', foodrivers.take_pickup, name='take_pickup'),
    ], 'classroom'), namespace='foodrivers')),

    path('foodonators/', include(([
        path('', foodonators.PickupListView.as_view(), name='orders'),
        path('pickup/add/', foodonators.PickupCreateView.as_view(), name='pickup_add'),
        path('pickup/<int:pk>/', foodonators.PickupUpdateView.as_view(), name='pickup_change'),
        path('pickup/<int:pk>/delete/', foodonators.PickupDeleteView.as_view(), name='pickup_delete'),
        path('pickup/<int:pk>/results/', foodonators.PickupResultsView.as_view(), name='pickup_results'),
        # path('pickup/<int:pk>/question/add/', foodonators.question_add, name='question_add'),
        # path('pickup/<int:quiz_pk>/question/<int:question_pk>/', foodonators.question_change, name='question_change'),
        # path('pickup/<int:pickup_pk>/question/<int:question_pk>/delete/', foodonators.QuestionDeleteView.as_view(), name='question_delete'),
    ], 'classroom'), namespace='foodonators')),
]
