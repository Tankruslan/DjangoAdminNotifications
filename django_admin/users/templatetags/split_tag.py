from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@stringfilter
def split(value, separators_str):
    space_separator = separators_str.split(",")[0]
    quotes_separator = separators_str.split(",")[1]
    actor = value.split(space_separator)[0]
    verb = value.split(space_separator)[1]
    action_object = value.split(quotes_separator)[1]
    response = actor.capitalize() + ' ' + verb + ' "{}"'.format(action_object)
    return response


register.filter('split', split)
