__author__ = 'Vincenzo Petrungaro'

from django import template
register = template.Library()


@register.filter
def to_currency(value):
    return float(value) / 100.0

@register.filter(name='ciao')
def ciao(value):
    return float(value) / 100.0

@register.filter
def as_percentage_of(part, whole):
    """ Use: Monkeys constitute {{ monkeys|as_percentage_of:animals }} of all animals."""
    try:
        return "%d%%" % (float(part) / whole * 100)
    except (ValueError, ZeroDivisionError):
        return ""

@register.filter(name='percentage')
def percentage(fraction, population):
    try:
        return "%.2f%%" % ((float(fraction) / float(population)) * 100)
    except ValueError:
        return ''

@register.filter(name='ap')
def ap(fraction, population):
    try:
        return "%.2f%%" % ((float(fraction) * float(population)))
    except ValueError:
        return ''