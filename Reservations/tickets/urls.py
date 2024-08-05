from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.user_login, name='login'),
    # Events
    path('event/all_events', login_required(views.event_list), name='event_list'),
    path('event/create/', login_required(views.create_event), name='create_event'),
    path('event/<int:event_id>/', login_required(views.event_detail), name='event_detail'),
    path('event/<int:event_id>/update/', login_required(views.update_event), name='update_event'),
    path('event/<int:event_id>/delete/', login_required(views.confirm_event_delete), name='confirm_event_delete'),

    # Reservations
    path('event/<int:event_id>/reserve/', login_required(views.reserve_tickets), name='reserve_tickets'),
    path('reservation/<int:reservation_id>/update/', login_required(views.update_reservation), name='update_reservation'),
    path('reservations/', login_required(views.user_reservations), name='reservations'),
    path('reservation/<int:reservation_id>/delete/', views.delete_reservation, name='delete_reservation'),

]
