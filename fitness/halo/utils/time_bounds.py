import pytz
from django.utils import timezone

#Daily booking bound
def get_daily_bounds(client_tz):

    '''
    Returns UTC start and end datetime for the current local day 
    based on the provided client timezone.
    '''
    now_utc = timezone.now()
    now_local = now_utc.astimezone(client_tz)

    start_local = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
    end_local = start_local + timezone.timedelta(days=1)

    return start_local.astimezone(pytz.UTC), end_local.astimezone(pytz.UTC)



#Weekly booking bound
def get_weekly_bounds(client_tz):

    '''
    Returns UTC start and end datetime for the current local week 
    based on the provided client timezone.
    '''
    now_utc = timezone.now()
    now_local = now_utc.astimezone(client_tz)

    start_local = now_local.replace(hour=0, minute=0, second=0, microsecond=0) - timezone.timedelta(days=now_local.weekday())
    end_local = start_local + timezone.timedelta(days=7)

    return start_local.astimezone(pytz.UTC), end_local.astimezone(pytz.UTC)
