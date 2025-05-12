from django.urls import path
from . import views


app_name = 'one_part'
urlpatterns = [
    path('all/', views.AllOnePartView.as_view(), name='all'),
    path('<slug>/', views.OnePartView.as_view(), name='one'),
    path('<slug>/save/', views.OnePartSaveView.as_view(), name='one-part-save'),
    path('<slug>/un-save/', views.OnePartUnSaveView.as_view(), name='one-part-un-save'),
]