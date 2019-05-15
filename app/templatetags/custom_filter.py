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
    return hasattr(value, "%s" % arg)

@register.filter
def user_type_check(value, arg):
    #"Is the current user's type entrepreneur or inverstor?"
    #if value.type == "0":
    #    print('Test entrepreneur')
    #else: 
    #    print('Test Investor')
    return hasattr(value, "%s" % arg)

@register.filter
def in_visible_fields(value):
    return not (value in ["Cover photo", "Background", "Solution", "Market",
                        "Business model", "Future", "Members", "Team desc",
                        "Pitching video link", "Product description", "Timeline"])

@register.filter
def summernote_fields(value):
    return value in ["Background", "Solution", "Market", "Business model", "Future"]
