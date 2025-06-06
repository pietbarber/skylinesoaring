from django.core.management.base import BaseCommand
from duty_roster.models import DutyAssignment
from django.utils.timezone import now
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = "Cancel unconfirmed ad-hoc ops days that are scheduled for tomorrow"

    def handle(self, *args, **kwargs):
        tomorrow = now().date() + timedelta(days=1)

        assignments = DutyAssignment.objects.filter(
            is_scheduled=False,
            is_confirmed=False,
            date=tomorrow
        )

        for assignment in assignments:
            ops_date = assignment.date.strftime("%A, %B %d, %Y")

            send_mail(
                subject=f"Ad-Hoc Ops Cancelled - {ops_date}",
                message=f"""Ad-hoc ops on {ops_date} could not get sufficient interest to meet the minimum 
duty crew of tow pilot and duty officer. The deadline has passed and the ops 
have been cancelled for tomorrow.\n\nCalendar: {settings.SITE_URL}/duty_roster/calendar/""",
                from_email="noreply@skylinesoaring.org",
                recipient_list=["members@skylinesoaring.org"],
            )

            self.stdout.write(self.style.WARNING(f"Cancelled unconfirmed ad-hoc ops day for {assignment.date}"))
            assignment.delete()
