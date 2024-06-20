from django import template
import re

register = template.Library()

@register.filter
def slugify(value):
    return re.sub(r'[\s]+', '-', value).lower()
