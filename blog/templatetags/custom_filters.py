from django import template

register = template.Library()

@register.filter
def limit_characters(value, max_length):
    if len(value) <= max_length:
        return value
    else:
        return value[:max_length]