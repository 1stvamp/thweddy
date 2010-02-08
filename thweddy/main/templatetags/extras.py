from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def setting(name):
    """Tag that provides access to properties from the django.settings
    dictionary.
    Usage:
        {% setting KEY %}
        where KEY is the key in the dictionary you want
    Values are returned as strings.
    """
    return str(settings.__getattr__(name))
