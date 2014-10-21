__author__ = 'Vincenzo Petrungaro'

from django import template
register = template.Library()

@register.filter(name='percentage')
def percentage(fraction, population):
    try:
        return "%.1f" % ((float(fraction) / float(population)) * 100)
    except ValueError:
        return '0.0'
    except:
        return '0.0'

@register.filter(name='percentuale')
def percentuale(fraction, population):
    try:
        return "%.1f%%" % ((float(fraction) / float(population)) * 100)
    except ValueError:
        return '0.0%'
    except:
        return "0.0%"

@register.filter(name='rapporto')
def rapporto(fraction, population):
    try:
        return "%f" % ((float(fraction) / float(population)))
    except ValueError:
        return ''

@register.filter(name='forbice_sup_of')
def forbice_sup_of(forbice, valore):
    try:
        f = float(valore) + float(forbice)
        if f <= 100:
            return "%.1f" % abs(f)
        else:
            return 100
    except ValueError:
        return ''

@register.filter(name='forbice_inf_of')
def forbice_inf_of(forbice, valore):
    try:
        f = float(valore) - float(forbice)
        if f >= 0:
            return "%.1f" % abs(f)
        else:
            return 0
    except ValueError:
        return ''

@register.filter(name='ap')
def ap(fraction, population):
    try:
        return "%i" % round((float(fraction) * float(population)))
    except ValueError:
        return ''