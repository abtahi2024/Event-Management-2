from django.urls import path
from users.views import sign_up, log_in, activate_user, log_out, admin_dashboard, organizer_dashboard, participant_dashboard, create_group, assign_role, view_group

urlpatterns = [
    path('sign-up/', sign_up, name="sign-up"),
    path('login/', log_in, name="login"),
    path('activate/<int:user_id>/<str:token>', activate_user, name="activate-user"),
    path('logout/', log_out, name="logout"),
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('organizer-dashboard/', organizer_dashboard, name='organizer-dashboard'),
    path('participant-dashboard/', participant_dashboard, name='participant-dashboard'),
    path('admin/create-group/', create_group, name="create-group"),
    path('admin/view-groups/', view_group, name="view-group"),
    path('admin/<int:user_id>/assign-role/', assign_role, name="assign-role"),
]