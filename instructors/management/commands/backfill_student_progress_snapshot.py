## instructors/management/commands/backfill_student_progress_snapshots.py

from django.core.management.base import BaseCommand
from members.constants.membership import DEFAULT_ACTIVE_STATUSES
from members.models import Member
from instructors.utils import update_student_progress_snapshot


class Command(BaseCommand):
    help = """
    Backfill StudentProgressSnapshot for all active members.

    This command iterates through every member whose membership_status
    is in DEFAULT_ACTIVE_STATUSES and rebuilds their progress snapshot.
    """

    def handle(self, *args, **options):
        # Fetch active members
        members = Member.objects.filter(
            membership_status__in=DEFAULT_ACTIVE_STATUSES
        )
        total = members.count()
        self.stdout.write(self.style.NOTICE(
            f"Starting backfill for {total} active members..."
        ))

        # Iterate and update
        for idx, member in enumerate(members, start=1):
            update_student_progress_snapshot(member)
            self.stdout.write(
                f"[{idx}/{total}] Updated snapshot for {member.full_display_name}"
            )

        self.stdout.write(self.style.SUCCESS(
            "Backfill complete: all StudentProgressSnapshot records updated."
        ))
