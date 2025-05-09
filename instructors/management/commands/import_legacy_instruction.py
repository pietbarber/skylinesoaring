# instructors/management/commands/import_legacy_instruction.py

import psycopg2
from django.core.management.base import BaseCommand
from django.conf import settings
from instructors.models import InstructionReport, LessonScore, GroundInstruction
from members.models import Member
from instructors.models import TrainingLesson
from django.utils.timezone import make_aware
from datetime import datetime
from tinymce.models import HTMLField  # in case it's needed
import logging

HTML_CUTOFF_EPOCH = 1171287324  # Reports before this should be <pre> wrapped

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import legacy instructor reports and ground instruction sessions"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Connecting to legacy database via settings.DATABASES['legacy']..."))

        legacy = settings.DATABASES['legacy']
        conn = psycopg2.connect(
            dbname=legacy['NAME'],
            user=legacy['USER'],
            password=legacy['PASSWORD'],
            host=legacy.get('HOST', ''),
            port=legacy.get('PORT', ''),
        )

        conn.set_client_encoding('WIN1252')  # <--- this is an official psycopg2 method

        cursor = conn.cursor()

        try:
            self.import_flight_instruction_reports(cursor)
            self.import_ground_instruction(cursor)
        finally:
            cursor.close()
            conn.close()

    def resolve_member(self, handle):
        try:
            return Member.objects.get(legacy_username__iexact=handle)
        except Member.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"❌ Member with legacy handle '{handle}' not found"))
            raise SystemExit(1)

    def import_flight_instruction_reports(self, cursor):
        self.stdout.write(self.style.NOTICE("Importing flight-based instruction reports..."))

        # Query legacy student_syllabus3 and instructor_reports2
        cursor.execute("""
            SELECT s.handle, s.number, s.mode, s.instructor, s.signoff_date,
                   r.report, r.lastupdated
            FROM student_syllabus3 s
            LEFT JOIN instructor_reports2 r
              ON s.handle = r.handle
             AND s.instructor = r.instructor
             AND s.signoff_date = r.report_date
        """)

        report_groups = {}
        for row in cursor.fetchall():
            handle, number, mode, instructor, date, report, lastupdated = row
            key = (handle, instructor, date)
            report_groups.setdefault(key, []).append((number, mode, report, lastupdated))

        for (handle, instructor, date), items in report_groups.items():
            student = self.resolve_member(handle)
            instructor_member = self.resolve_member(instructor)

            # Check if report already exists
            report_obj, created = InstructionReport.objects.get_or_create(
                student=student,
                instructor=instructor_member,
                report_date=date,
                defaults={'report_text': ''}
            )

            for number, mode, report_html, updated in items:
                lesson = TrainingLesson.objects.get(code=number)
                LessonScore.objects.update_or_create(
                    report=report_obj,
                    lesson=lesson,
                    defaults={'score': mode}
                )

                # If this row carries the actual narrative...
                if report_html:
                    if updated is not None and updated < HTML_CUTOFF_EPOCH:
                        new_report_text = f"<pre>{report_html}</pre>"
                    else:
                        new_report_text = report_html
                    if report_obj.report_text != new_report_text:
                        report_obj.report_text = new_report_text
                        report_obj.save()
                        print("✍️ updated narrative", end="", flush=True)

            status = "✅ Created" if created else "↺ Updated"
            self.stdout.write(f"{status}: {student} / {instructor_member} / {date}")

    def import_ground_instruction(self, cursor):
        from instructors.models import GroundLessonScore  # local import to avoid circularity
    
        self.stdout.write(self.style.NOTICE("Importing ground instruction sessions..."))
    
        cursor.execute("""
            SELECT pilot, instructor, inst_date, duration, location, ground_tracking_id
            FROM ground_inst
        """)
        sessions = cursor.fetchall()
    
        for pilot, instructor, date, duration, location, tracking_id in sessions:
            student = self.resolve_member(pilot)
            instructor_member = self.resolve_member(instructor)
    
            gi, created = GroundInstruction.objects.get_or_create(
                student=student,
                instructor=instructor_member,
                date=date,
                defaults={
                    'location': location,
                    'duration': duration,
                    'notes': ''
                }
            )
    
            # Attach notes from instructor_reports2 — only if not used in InstructionReport
            cursor.execute("""
                SELECT report
                FROM instructor_reports2
                WHERE handle = %s AND instructor = %s AND report_date = %s
            """, (pilot, instructor, date))
            row = cursor.fetchone()
    
            if row and row[0]:
                legacy_report_text = row[0].strip()
    
                # Check for deduplication: is this report already in a flight record?
                exists = InstructionReport.objects.filter(
                    student=student,
                    instructor=instructor_member,
                    report_date=date,
                    report_text__iexact=legacy_report_text
                ).exists()
    
                if not exists and (gi.notes or '').strip() != legacy_report_text:
                    gi.notes = legacy_report_text
                    gi.save()
                    print("📝 Ground essay attached", end="", flush=True)
    
            status = "✅ Created" if created else "↺ Skipped (exists)"
            self.stdout.write(f"{status}: {student} / {instructor_member} / {date}")
