from django.urls import path
from . import views

urlpatterns = {
    path('', views.dashboard, name='Home'),
    path('select_state', views.state_wise, name='Home'),
    # path('update_select_state', views.update_state_wise, name='Home'),
    path('all_over_india', views.dashboard, name='Home'),
}
