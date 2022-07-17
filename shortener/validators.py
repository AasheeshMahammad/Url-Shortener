from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def validate_url(value):
    url_validator = URLValidator()
    new_value = value
    if "http" not in value:
        new_value = 'http://' + value
    try:
        url_validator(new_value)
    except:
        raise ValidationError("Invalid URL for this field")
    return new_value

def validate_dot_com(value):
    if not "com" in value:
        raise ValidationError("This is not valid becuase of no .com")
    return value