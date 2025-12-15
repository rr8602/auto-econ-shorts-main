from datetime import datetime, timedelta, timezone

def get_kst_hour() -> int:
    kst = timezone(timedelta(hours=9))
    return datetime.now(kst).hour
