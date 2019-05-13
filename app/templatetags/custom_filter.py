from django import template

register = template.Library()

@register.filter
def get_attr(value, arg):
    if hasattr(value, str(arg)):
        return getattr(value, arg)
    elif hasattr(value, 'has_key') and value.has_key(arg):
        return value[arg]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    else:
        return None

@register.filter
def user_has(value, arg):
    "Has the current user done the `arg` action on the `value` object?"
    user = globals.user
    if user.is_authenticated() and hasattr(value, "user_has_%s" % arg):
        return getattr(value, "user_has_%s" % arg)(user)
    else:
        return False
