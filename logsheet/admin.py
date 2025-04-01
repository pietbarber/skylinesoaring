from django.contrib import admin
from .models import Glider, Towplane, Logsheet, Flight, RevisionLog, TowRate, Airfield
from django.utils.html import format_html

# Admin configuration for managing Towplane objects
# Use this to add more club tow planes. 
# Each time we have a new tow plane, we need to add an object
# with the admin interface here. 
@admin.register(Towplane)
class TowplaneAdmin(admin.ModelAdmin):
    list_display = ("name", "registration", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "registration")


# Admin configuration for Glider objects. 
# Use this to add more gliders to the system.
# If a new glider is acquired by the club, we need to add it here.
# If a member gets a new glider, it also needs to be added here. 
# If the rental rate for any of our gliders change, those updates need to go here. 
@admin.register(Glider)
class GliderAdmin(admin.ModelAdmin):
    list_display = ("competition_number", "n_number", "model", "make", "seats")
    search_fields = ("competition_number", "n_number", "model", "make")

# The flight table is where most of the action for the logsheet lives. 
# This is a stop-gap to edit the database directly from the admin interface, 
# used only when there is a problem with the app that we can't fix. 
# This is kind of an ugly view in admin, because if we have a zillion flights, 
# they're all going to be listed here. I don't have any better solutions. 
@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ("logsheet", "launch_time", "landing_time", "pilot", "instructor", 
                    "glider", "towplane", "tow_pilot", "tow_cost_actual", "rental_cost_actual")
    list_filter = ("logsheet", "glider", "towplane", "instructor")
    search_fields = ("pilot__first_name", "pilot__last_name", "instructor__first_name", "instructor__last_name")
    readonly_fields = ("tow_cost", "rental_cost", "total_cost_display")
    def tow_cost(self, obj):
        return obj.tow_cost_display

    def rental_cost(self, obj):
        return obj.rental_cost_display

    def total_cost_display(self, obj):
        return obj.total_cost_display

# Each time a member locks a flight log because it's finalized, no more changes can be done
# to that flight log.  Of course, mistakes happen, and the log sheet needs to be revised. 
# A superuser can unlock the finalized boolean to allow edits to that logsheet again. 
# But each time that happens, a log entry gets added into this RevisionLog model.
# The admin mode is here in case you need to scrub or edit any of those.  Maybe this 
# entry in admin.py shouldn't even exist? 
@admin.register(RevisionLog)
class RevisionLogAdmin(admin.ModelAdmin):
    list_display = ("logsheet", "revised_by", "revised_at")
    list_filter = ("revised_by", "revised_at")

# Each time the club operates at a new field for the first time, it needs to be added here. 
# When we start a logsheet for the day, we need to indicate the airfield where the operations take place. 
# If we as a club are starting an op at a new airfield, we need to add it here first. This is the only place 
# to add it. 
@admin.register(Airfield)
class AirfieldAdmin(admin.ModelAdmin):
    list_display = ['identifier', 'name', 'is_active']
    search_fields = ['identifier', 'name']
    list_filter = ['is_active']
    readonly_fields = ['airfield_image_preview']

    def airfield_image_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height: 150px;" />', obj.photo.url)
        return "(No photo uploaded)"
    airfield_image_preview.short_description = "Current Photo"

# The particulars of what day a logsheet happened, the airfield, who is on the duty roster for that day
# are all kept in teh Logsheet model. If a logsheet is finalized is kept in this entry too. 
# One manual way to unfinalize a logsheet (open it up fo revisions) is to just flip the boolean in this
# table with this admin interface.  This isn't ideal. 
@admin.register(Logsheet)
class LogsheetAdmin(admin.ModelAdmin):
    list_display = ("log_date", "airfield", "created_by", "finalized", "created_at")
    list_filter = ("airfield", "finalized")
    search_fields = ("airfield__name", "created_by__username")


# The prices for tows to different altitudes are stored here. 
# Currently all tows are at the same rate for all tow planes, which could be a 
# problem in the future if we have some other tow plane come tow for us, 
# and they charge different rates. I'll have to think about it. 
# Also unfortunately, the prices are recorded in 100 feet increments, which is not very user-friendly.
# There is a script in the logsheet/management that allows you to paste the output into
# a `./manage.py shell` command

@admin.register(TowRate)
class TowRateAdmin(admin.ModelAdmin):
    list_display = ("altitude", "price")
    list_editable = ("price",)
    ordering = ("altitude",)
