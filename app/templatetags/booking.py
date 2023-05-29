import datetime
from django import template

register = template.Library()


@register.simple_tag
def is_1hour_later(dt, hour):
    later_1hour = datetime.datetime.now() + datetime.timedelta(hours=1)
    target = datetime.datetime.combine(dt, datetime.time(hour=hour.hour, minute=hour.minute, second=0))
    return later_1hour <= target
