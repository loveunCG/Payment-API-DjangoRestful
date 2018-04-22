from django.urls import path

from . import views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('ajax_get_incoming_table/', views.get_incoming_table, name='get_incoming_table'),
    path('ajax_get_outcoming_table/', views.get_outcoming_table, name='get_outcoming_table'),
    path('ajax_update_notification/', views.update_notification, name='update_notification'),
]