from django import template
register = template.Library()
@register.filter()
def is_numeric(value):
    return value.isdigit()
