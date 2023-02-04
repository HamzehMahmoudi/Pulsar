from django.core.validators import ValidationError
from django.utils.translation import gettext_lazy as _
import re

error_messages = {
    'username_invalid':_('Username invalid'),
}


def validate_username(user_name):
    # init a username pattern
    ## Only starts and ends with char or number
    ## Has 8-20 characters
    ## Only _ and __ are allowed
    user_name_pattern = re.compile(r"^(?=[a-zA-Z0-9_]{5,20}$)(?!.*_{3})[^_].*[^_]$")
    if not re.search(user_name_pattern,user_name):
        raise ValidationError(error_messages['username_invalid'],code='username_invalid')
