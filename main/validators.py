from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def validate_comma_separated(string):
    try:
        string.split(',')

    except:
        raise ValidationError(
            _('The input must be a string of comma-separated fields.'),
        )

    if '[' in string or ']' in string:
        raise ValidationError(
            _('Do not use "[ ]". Just separate the values by comma.'),
        )


def validate_command(string):
    checklist = ['>', '>>', '&']
    if [x for x in checklist if x in string]:
        raise ValidationError(
            _('You are not allowed to use [ ' + ' or '.join(checklist) + ' ] in your command'),
        )