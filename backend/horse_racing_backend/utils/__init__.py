import pytz
from datetime import datetime, timedelta, time

### timezone = "Australia/Sydney"
def getTimeOffset(timezone):
    try:
        tz = pytz.timezone(timezone)
        current_offset = tz.localize(datetime.now()).utcoffset()
        return current_offset.seconds/3600
    except KeyError:
        return None

### timezone = "Australia/Sydney"
def getCountryCode(timezone):
    for country_code, timezones in pytz.country_timezones.items():
        if timezone in timezones:
            return country_code
    return None

### timezone = "Australia/Sydney"
def getTimeRageInADay(timezone):
    offset = getTimeOffset (timezone)
    if offset is None: offset = 0
    # Get the current date in GMT
    gmt_timezone = pytz.timezone('GMT')
    current_date_gmt = datetime.now(gmt_timezone).date()

    # Create the start and end time for the time range
    start_time = datetime.combine(current_date_gmt, time.min)
    end_time = datetime.combine(current_date_gmt, time.max)

    # Convert the start and end time to GMT
    start_time_gmt = gmt_timezone.localize(start_time)
    end_time_gmt = gmt_timezone.localize(end_time)

    start_time_gmt -= timedelta(hours=offset)
    end_time_gmt -= timedelta(hours=offset)

    return [start_time_gmt, end_time_gmt]
