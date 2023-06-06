from django import template

register = template.Library()


@register.simple_tag
def get_dishes_for_weekday(menu, weekday_name):
    return menu.get_dishes_for_weekday(weekday_name)
