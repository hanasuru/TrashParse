from __future__ import division
from datetime import datetime, timedelta, tzinfo
from calendar import timegm

EPOCH_AS_FILETIME = 116444736000000000  # January 1, 1970 as MS file time
HUNDREDS_OF_NANOSECONDS = 10000000
HOUR = timedelta(hours=1)


class UTC(tzinfo):
    def utcoffset(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return timedelta(0)


class UTCTime(object):
    @staticmethod
    def time_to_date(ft):
        try:
            return datetime.utcfromtimestamp((ft - EPOCH_AS_FILETIME) / HUNDREDS_OF_NANOSECONDS)
        except ValueError:
            return 'year is out of range'

    @staticmethod
    def date_to_time(dt):
        if (dt.tzinfo is None) or (dt.tzinfo.utcoffset(dt) is None):
            dt = dt.replace(tzinfo=utc)
    
        return EPOCH_AS_FILETIME + (timegm(dt.timetuple()) * HUNDREDS_OF_NANOSECONDS)