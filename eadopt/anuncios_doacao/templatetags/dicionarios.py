from django import template

register = template.Library()

@register.filter
def keyvalue(dict, key):    
    try:
        return dict[key]
    except KeyError:
        return ''
        
@register.filter
def count(dict):
    return len(dict)
