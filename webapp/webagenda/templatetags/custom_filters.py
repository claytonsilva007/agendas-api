from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    """Retorna o valor do dicionário usando a chave"""
    return d.get(key, None)
