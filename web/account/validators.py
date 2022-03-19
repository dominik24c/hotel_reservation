from django.core import validators

only_letters = validators.RegexValidator('^[a-zA-Z ]*$', 'Only letters are allowed.')
alphanumeric = validators.RegexValidator('^[a-zA-Z0-9 ]*$', 'Alphanumeric is allowed.')
