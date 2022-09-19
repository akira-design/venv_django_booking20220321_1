from django.template import Library
register = Library()

@register.filter
def in_group(user, group_name):
    if user.groups.filter(name=group_name).exists():
        return True
    else:
        return False