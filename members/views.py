from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from .models import Member
from .forms import MemberForm

def is_instructor(user):
    return user.is_authenticated and user.is_instructor

@login_required
def duty_roster(request):
    return render(request, 'members/duty_roster.html')

@login_required
@user_passes_test(is_instructor)
def instructors_only(request):
    return render(request, 'members/instructors.html')

@login_required
def members_list(request):
    return render(request, 'members/members.html')

@login_required
def log_sheets(request):
    return render(request, 'members/log_sheets.html')

@login_required
def member_list(request):
    members = Member.objects.all()
    return render(request, "members/member_list.html", {"members": members})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Membership Officers').exists(), login_url='/')
def member_edit(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == "POST":
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('member_list')
    else:
        form = MemberForm(instance=member)
    return render(request, "members/member_edit.html", {"form": form, "member": member})


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Member
from .forms import MemberForm

@login_required
def member_edit(request, pk):
    member = get_object_or_404(Member, pk=pk)

    # If the user isn't staff and they're trying to edit someone else:
    if not request.user.is_staff and request.user.pk != member.pk:
        return redirect('member_list')  # or return 403 if you prefer

    if request.method == "POST":
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('member_list')
    else:
        form = MemberForm(instance=member)

    return render(request, "members/member_edit.html", {"form": form, "member": member})
