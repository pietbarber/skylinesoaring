from django.shortcuts import render
from .decorators import instructor_required
from .models import TrainingLesson, SyllabusDocument, TrainingPhase

# instructors/views.py
@instructor_required
def instructors_home(request):
    return render(request, "instructors/instructors_home.html")


@instructor_required
def syllabus_overview(request):
    lessons = TrainingLesson.objects.all().order_by("code")
    return render(request, "instructors/syllabus_overview.html", {"lessons": lessons})

@instructor_required
def syllabus_overview_grouped(request):
    phases = TrainingPhase.objects.prefetch_related("lessons").all()
    header = SyllabusDocument.objects.filter(slug="header").first()
    materials = SyllabusDocument.objects.filter(slug="materials").first()

    return render(request, "instructors/syllabus_grouped.html", {
        "phases": phases,
        "header": header,
        "materials": materials,
    })

from django.shortcuts import render, get_object_or_404

@instructor_required
def syllabus_detail(request, code):
    lesson = get_object_or_404(TrainingLesson, code=code)
    return render(request, "instructors/syllabus_detail.html", {"lesson": lesson})


from datetime import datetime
from collections import defaultdict
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils.timezone import now
from django.http import HttpResponseBadRequest
from django.forms import formset_factory

from instructors.decorators import instructor_required
from instructors.forms import InstructionReportForm, LessonScoreSimpleForm, LessonScoreSimpleFormSet
from instructors.models import InstructionReport, LessonScore, TrainingLesson
from members.models import Member

@instructor_required
def fill_instruction_report(request, student_id, report_date):
    try:
        report_date = datetime.strptime(report_date, "%Y-%m-%d").date()
    except ValueError:
        return HttpResponseBadRequest("Invalid report date format.")

    student = get_object_or_404(Member, pk=student_id)
    instructor = request.user

    report, created = InstructionReport.objects.get_or_create(
        student=student, instructor=instructor, report_date=report_date
    )

    if report_date > now().date():
        return HttpResponseBadRequest("Report date cannot be in the future.")

    lessons = TrainingLesson.objects.all().order_by("code")

    if request.method == "POST":
        report_form = InstructionReportForm(request.POST, instance=report)
        formset = LessonScoreSimpleFormSet(request.POST)

        if report_form.is_valid() and formset.is_valid():
            report_form.save()
            LessonScore.objects.filter(report=report).delete()

            for form in formset.cleaned_data:
                lesson = form.get("lesson")
                score = form.get("score")
                if lesson and score:
                    LessonScore.objects.create(report=report, lesson=lesson, score=score)

            messages.success(request, "Instruction report submitted successfully.")
            return redirect("instructors:syllabus_overview")
        else:
            messages.error(request, "There were errors in the form. Please review and correct them.")
            print("Report form errors:", report_form.errors)
            print("Formset errors:", formset.errors)

    else:
        # GET request
        report_form = InstructionReportForm(instance=report)
        initial_data = []
        lesson_objects = []

        for lesson in lessons:
            existing_score = LessonScore.objects.filter(report=report, lesson=lesson).first()
            initial_data.append({
                "lesson": lesson.id,
                "score": existing_score.score if existing_score else "",
            })
            lesson_objects.append(lesson)
        
        formset = LessonScoreSimpleFormSet(initial=initial_data)

        # Bundle each form with its lesson
        form_rows = list(zip(formset.forms, lesson_objects))


    return render(request, "instructors/fill_instruction_report.html", {
        "student": student,
        "report_form": report_form,
        "formset": formset,
        "form_rows": form_rows,
        "report_date": report_date,
    })


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from logsheet.models import Flight, Logsheet
from members.models import Member
from datetime import timedelta
from django.utils import timezone
from collections import defaultdict

@login_required
def select_instruction_date(request, student_id):
    instructor = request.user
    student = get_object_or_404(Member, pk=student_id)

    today = timezone.now().date()

    recent_flights = Flight.objects.filter(
        instructor=instructor,
        pilot=student
    ).select_related("logsheet")

    # Use correct logsheet date field
    recent_flights = [f for f in recent_flights if f.logsheet.log_date <= today]

    # Group by date
    flights_by_date = defaultdict(list)
    for flight in recent_flights:
        flights_by_date[flight.logsheet.log_date].append(flight) 

    sorted_dates = sorted(flights_by_date.items(), reverse=True)

    context = {
        "student": student,
        "flights_by_date": sorted_dates,
        "today": today,
    }
    return render(request, "instructors/select_instruction_date.html", context)

from django.shortcuts import get_object_or_404, render
from instructors.models import InstructionReport, LessonScore, TrainingLesson
from members.models import Member
from collections import defaultdict

def member_training_grid(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    reports = InstructionReport.objects.filter(student=member).order_by("report_date").prefetch_related("lesson_scores__lesson")
    lessons = TrainingLesson.objects.all().order_by("code")

    # Dates of instruction sessions (chronological)
    report_dates = [r.report_date for r in reports]

    # Build grid: lesson -> {date -> score}
    lesson_data = []
    for lesson in lessons:
        score_map = {}
        for report in reports:
            score = report.lesson_scores.filter(lesson=lesson).first()
            score_map[report.report_date] = score.score if score else ""

        max_score = max((s for s in score_map.values() if s.isdigit()), default="")
        lesson_data.append({
            "label": f"{lesson.code} – {lesson.title}",
            "scores": [score_map[d] for d in report_dates],
            "max_score": max_score
        })

    context = {
        "member": member,
        "lesson_data": lesson_data,
        "report_dates": report_dates,
    }
    return render(request, "shared/training_grid.html", context)


