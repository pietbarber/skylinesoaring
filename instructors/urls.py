from django.urls import path
from . import views

app_name = "instructors"

urlpatterns = [
    path("", views.instructors_home, name="index"),
    path("syllabus/", views.syllabus_overview, name="syllabus_overview"),
    path("syllabus/grouped/", views.syllabus_overview_grouped, name="syllabus_grouped"),

]

