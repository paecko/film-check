from django import template

register = template.Library()

@register.filter(name='times')
def times(number):
    return range(number)

@register.filter(name='my_abs')
def my_abs(number):
    return abs(number)

@register.filter(name='update_variable')
def update_variable(value):
    data = value
    return data