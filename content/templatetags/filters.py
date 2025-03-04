from django import template

register = template.Library()

@register.filter(name='get')
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def kilo_to_grams(value):
    return round(value * 1000)

@register.filter
def multiply(num1, num2):
    return round(num1 * num2, 2)