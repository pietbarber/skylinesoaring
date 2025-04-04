import logging
import psycopg2
from django.conf import settings
from django.core.management.base import BaseCommand
from members.models import Member, Badge, MemberBadge
from datetime import date

logger = logging.getLogger(__name__)

BADGE_NAME_MAP = {
    'A': 'A Badge',
    'B': 'B Badge',
    'C': 'C Badge',
    'Silver Badge': 'FAI Silver Badge',
    'Gold Badge': 'FAI Gold Badge',
    'Diamond Badge': 'FAI Diamond Badge',
    'Silver Distance': 'Silver Distance',
    'Silver Altitude': 'Silver Altitude',
    'Silver Duration': 'Silver Duration',
    'Gold Distance': 'Gold Distance',
    'Gold Altitude': 'Gold Altitude',
    'Diamond Distance': 'Diamond Distance',
    'Diamond Altitude': 'Diamond Altitude',
    'Diamond Goal': 'Diamond Goal',
    'Bronze Badge': 'Bronze Badge',
}

class Command(BaseCommand):
    help = "Import earned member badges from the legacy 'badges_earned' table"

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Run without saving changes')

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        self.stdout.write(self.style.NOTICE("Connecting to legacy database via settings.DATABASES['legacy']..."))

        legacy = settings.DATABASES['legacy']
        conn = psycopg2.connect(
            dbname=legacy['NAME'],
            user=legacy['USER'],
            password=legacy['PASSWORD'],
            host=legacy.get('HOST', ''),
            port=legacy.get('PORT', ''),
        )
        conn.set_client_encoding('WIN1252')

        with conn.cursor() as cursor:
            cursor.execute("SELECT handle, badge, earned_date FROM badges_earned")
            rows = cursor.fetchall()

        imported = 0
        skipped = 0

        for handle, badge_name, earned_date in rows:
            handle = handle.strip()
            badge_name = badge_name.strip()
            badge_name = BADGE_NAME_MAP.get(badge_name, badge_name)

            try:
                member = Member.objects.get(legacy_username=handle)
            except Member.DoesNotExist:
                logger.warning(f"No member found for handle '{handle}', skipping badge '{badge_name}'")
                skipped += 1
                continue

            try:
                badge = Badge.objects.get(name__iexact=badge_name)
            except Badge.DoesNotExist:
                logger.warning(f"Badge '{badge_name}' not found, skipping for {handle}")
                skipped += 1
                continue

            if dry_run:
                self.stdout.write(f"[DRY RUN] Would assign {badge_name} to {member}")
            else:
                mb, created = MemberBadge.objects.get_or_create(
                    member=member,
                    badge=badge,
                    defaults={
                        'date_awarded': earned_date or date.today(),
                        'notes': ''
                    }
                )
                if created:
                    self.stdout.write(f"Assigned {badge_name} to {member}")
                else:
                    self.stdout.write(f"{badge_name} already exists for {member}, skipping")
            imported += 1

        self.stdout.write(self.style.SUCCESS(
            f"Import complete. Total processed: {imported + skipped}, Imported: {imported}, Skipped: {skipped}"
        ))
