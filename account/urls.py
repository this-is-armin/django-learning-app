from django.urls import path
from . import views


app_name = 'account'
urlpatterns = [
    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),
    path('sign-in/', views.SignInView.as_view(), name='sign-in'),
    path('sign-out/', views.SignOutView.as_view(), name='sign-out'),
    path('forget-password/', views.ForgetPasswordView.as_view(), name='forget-password'),

    path('<username>/', views.ProfileView.as_view(), name='profile'),

    path('<username>/saved-courses/', views.SavedCoursesView.as_view(), name='saved-courses'),
    path('<username>/saved-one-parts/', views.SavedOnePartsView.as_view(), name='saved-one-parts'),
]