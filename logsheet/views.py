from django.shortcuts import render
from members.decorators import active_member_required

@active_member_required
def index(request):
    return render(request, "logsheet/index.html")

from django.shortcuts import render, redirect
from .forms import CreateLogsheetForm
from .models import Logsheet
from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Logsheet
from .forms import CreateLogsheetForm
from members.decorators import active_member_required

@active_member_required
def create_logsheet(request):
    if request.method == "POST":
        form = CreateLogsheetForm(request.POST)
        if form.is_valid():
            log_date = form.cleaned_data['log_date']
            location = form.cleaned_data['location']

            # Check if one already exists
            existing = Logsheet.objects.filter(log_date=log_date, location=location).first()
            if existing:
                messages.info(request, f"A logsheet for {log_date} at {location} already exists.")
                return redirect("logsheet:manage", pk=existing.pk)

            # No duplicate, so go ahead and create
            logsheet = form.save(commit=False)
            logsheet.created_by = request.user
            logsheet.save()

            messages.success(request, f"Logsheet created for {log_date} at {location}")
            return redirect("logsheet:manage", pk=logsheet.pk)
    else:
        form = CreateLogsheetForm()

    return render(request, "logsheet/start_logsheet.html", {"form": form})

from .forms import FlightForm

@active_member_required
def manage_logsheet(request, pk):
    logsheet = get_object_or_404(Logsheet, pk=pk)

    if request.method == "POST":
        form = FlightForm(request.POST)
        if form.is_valid():
            flight = form.save(commit=False)
            flight.logsheet = logsheet
            flight.save()
            messages.success(request, "Flight added successfully.")
            return redirect("logsheet:manage", pk=logsheet.pk)
    else:
        form = FlightForm(initial={"field": logsheet.location})

    return render(request, "logsheet/logsheet_manage.html", {
        "logsheet": logsheet,
        "form": form,
    })

@active_member_required
def list_logsheets(request):
    logsheets = Logsheet.objects.order_by("-log_date", "-created_at")
    return render(request, "logsheet/logsheet_list.html", {
        "logsheets": logsheets,
    })
