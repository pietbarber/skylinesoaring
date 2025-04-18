from django.urls import path
from . import views

app_name = "instructors"

urlpatterns = [
    path("", views.instructors_home, name="index"),
    path("syllabus/", views.syllabus_overview_grouped, name="syllabus_overview"),
    path("syllabus/<str:code>/", views.syllabus_detail, name="syllabus_detail"),
    path("report/select-date/<int:student_id>/", views.select_instruction_date, name="select_instruction_date"),
    path("report/<int:student_id>/<slug:report_date>/", views.fill_instruction_report, name="fill_instruction_report"),
    path("training-grid/<int:member_id>/", views.member_training_grid, name="member_training_grid"),
    path("instruction-record/<int:member_id>/", views.member_instruction_record, name="member_instruction_record"),
    path("log-ground-instruction/", views.log_ground_instruction, name="log_ground_instruction"),
    path("assign-qualification/<int:member_id>/", views.assign_qualification, name="assign_qualification"),

]


