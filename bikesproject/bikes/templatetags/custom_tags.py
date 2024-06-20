from django import template

register = template.Library()

@register.filter
def is_active_page(url_name,page_names):
    return 'active' if url_name in page_names.split(',') else ''
