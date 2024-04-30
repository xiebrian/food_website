from django import template

register = template.Library()

@register.filter(name='duration')
def duration(td):
    """ Converts a DurationField object into a human-readable form """
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    if hours == 0:
        return "{} min".format(minutes)
    elif minutes == 0:
        return "{} hr".format(hours)
    else:
        return "{} hr {} min".format(hours, minutes)

@register.filter()
def is_numeric(value):
    return value.isdigit()
