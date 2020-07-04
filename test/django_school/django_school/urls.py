from django.urls import include, path

from classroom.views import classroom, foodrivers, foodonators

urlpatterns = [
    path('', include('classroom.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', classroom.SignUpView.as_view(), name='signup'),
    path('accounts/signup/foodriver/', foodrivers.FoodriverSignUpView.as_view(), name='foodriver_signup'),
    path('accounts/signup/foodonator/', foodonators.FoodonatorSignUpView.as_view(), name='foodonator_signup'),
    # path('accounts/signup/shelter/', shelters.ShelterSignUpView.as_view(), name='shelter_signup'),
]
