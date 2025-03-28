from django.db import models
from members.models import Member

class Logsheet(models.Model):
    log_date = models.DateField()
    location = models.CharField(max_length=100)
    created_by = models.ForeignKey(Member, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    finalized = models.BooleanField(default=False)

    class Meta:
        unique_together = ("log_date", "location")

    def __str__(self):
        return f"{self.log_date} @ {self.location}"
    
    from django.db import models

class Flight(models.Model):
    logsheet = models.ForeignKey("Logsheet", on_delete=models.CASCADE, related_name="flights")
    launch_time = models.TimeField()
    landing_time = models.TimeField(blank=True, null=True)
    pilot = models.ForeignKey("members.Member", on_delete=models.SET_NULL, null=True, related_name="flights_as_pilot")
    instructor = models.ForeignKey("members.Member", on_delete=models.SET_NULL, null=True, blank=True, related_name="flights_as_instructor")
    glider = models.ForeignKey("members.Glider", on_delete=models.SET_NULL, null=True)
    tow_pilot = models.ForeignKey("members.Member", on_delete=models.SET_NULL, null=True, blank=True, related_name="flights_as_tow_pilot")
    towplane = models.ForeignKey("Towplane", on_delete=models.SET_NULL, null=True, blank=True)
    field = models.CharField(max_length=100)  # Copy from logsheet or input per-flight
    flight_type = models.CharField(max_length=50)  # dual, solo, intro, etc.
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pilot} in {self.glider} at {self.launch_time}"
    
    from django.db import models
from members.models import Member

class RevisionLog(models.Model):
    logsheet = models.ForeignKey("Logsheet", on_delete=models.CASCADE, related_name="revisions")
    revised_by = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    revised_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"Revised by {self.revised_by} on {self.revised_at}"

class Towplane(models.Model):
    name = models.CharField(max_length=100)
    registration = models.CharField(max_length=50)  # e.g., N-number
    photo = models.ImageField(upload_to="towplane_photos/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        ordering = ["name"]

    def __str__(self):
        status = " (Inactive)" if not self.is_active else ""
        return f"{self.name} ({self.registration})"

