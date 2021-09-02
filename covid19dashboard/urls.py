from django.urls import path
from covid19dashboard import views

urlpatterns = [
    path('', views.index),
    path('select_state', views.state_wise, name='Home'),
    path('all_over_india', views.index, name='Home'),
]
