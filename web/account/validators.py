from django.core import validators

only_letters = validators.RegexValidator(r'^[a-zA-Z]*$', 'Only alpha letters are allowed.')
