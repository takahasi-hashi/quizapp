# quizapp/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def index(sequence, position):
    try:
        return sequence[position]
    except:
        return ''
