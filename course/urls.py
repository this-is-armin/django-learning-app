from django.urls import path
from . import views


app_name = 'course'
urlpatterns = [
    path('all/', views.AllCoursesView.as_view(), name='all'),
    path('<slug>/', views.CourseView.as_view(), name='one'),
    path('<slug>/save/', views.CourseSaveView.as_view(), name='save'),
    path('<slug>/un-save/', views.CourseUnSaveView.as_view(), name='un-save'),
    path('<slug>/<counter>/', views.EpisodeView.as_view(), name='episode'),
]