from django import template

register = template.Library()


@register.filter(name='getattr')
def getattr(jsonData, key):
    return jsonData.get(key)
