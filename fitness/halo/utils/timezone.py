import pytz
from datetime import datetime

def convert_ist_to_utc(ist_datetime_str):

    #Takes datetime in IST and returns it in UTC datetime.
    naive_dt = datetime.strptime(ist_datetime_str, "%Y-%m-%d %I:%M %p")
    ist = pytz.timezone('Asia/Kolkata')
    ist_dt = ist.localize(naive_dt)
    return ist_dt.astimezone(pytz.UTC)


def get_client_timezone(request):
    #Extracts client's timezone from query param, returns pytz timezone
    #Falls back to UTC if invalid or missing

    tzname = request.GET.get('tz')
    try:
        return pytz.timezone(tzname) if tzname else pytz.UTC
    except Exception:
        return pytz.UTC