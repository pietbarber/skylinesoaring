# logsheet/utils/aliases.py
# This file can be safely removed after we backfill from the legacy database. 

from logsheet.models import Towplane

TOWPLANE_ALIASES = [
    {"name": "SSC Pawnee", "start": "2000-01-01", "end": "2017-10-08", "registration": "N90866"},
    {"name": "SSC Pawnee", "start": "2017-10-09", "end": "2099-12-31", "registration": "N424BY"},
    {"name": "SSC Husky", "start": "2000-01-01", "end": "2099-12-31", "registration": "N8085S"},
    {"name": "SSC Huskey", "start": "2000-01-01", "end": "2099-12-31", "registration": "N8085S"},
    {"name": "Other", "start": "2000-01-01", "end": "2099-12-31", "registration": "OTHER"},
    {"name": "Burner Citabria", "start": "2000-01-01", "end": "2099-12-31", "registration": "OTHER"},
    {"name": "Other Tow Plane NA", "start": "2000-01-01", "end": "2099-12-31", "registration": "OTHER"},
    {"name": "SVS Pawnee N7298Z", "start": "2000-01-01", "end": "2099-12-31", "registration": "OTHER"},
    {"name": "Stahl Towplane", "start": "2000-01-01", "end": "2099-12-31", "registration": "OTHER"},
    {"name": "Stahl Skyhawk N5323R", "start": "2000-01-01", "end": "2099-12-31", "registration": "OTHER"},
    {"name": "M-ASA Super Cub", "start": "2000-01-01", "end": "2099-12-31", "registration": "OTHER"},
    {"name": "Soaring 100", "start": "2000-01-01", "end": "2099-12-31", "registration": "OTHER"},
    {"name": "SSC Friend", "start": "2000-01-01", "end": "2099-12-31", "registration": "OTHER"},
    {"name": "ESC Winch Launch NA", "start": "2000-01-01", "end": "2099-12-31", "registration": "WINCH"},
    {"name": "Self Launch", "start": "2000-01-01", "end": "2099-12-31", "registration": "SELF"},
]

def resolve_towplane(name, flight_date, comment=""):
    name = (name or "").strip()
    comment = (comment or "").lower()

    if not name:
        # Handle known winch week
        if flight_date.year == 2021 and flight_date.month == 9:
            return None
        # Handle canceled ops with explanation
        if any(kw in comment for kw in ["canceled", "no ops", "weather", "wind"]):
            return None
        print(f"⚠️  Blank towplane with no clear reason on {flight_date}")
        return None

    for entry in TOWPLANE_ALIASES:
        if entry["name"].lower() == name.lower() and entry["start"] <= str(flight_date) <= entry["end"]:
            return Towplane.objects.filter(registration=entry["registration"]).first()

    print(f"⚠️  Could not resolve towplane '{name}' on {flight_date}")
    return None
