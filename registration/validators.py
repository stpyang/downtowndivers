'''Copyright 2016 DDNY. All Rights Reserved.'''

from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

def validate_user(user):
    if User.objects.get(id=user).is_superuser:
        raise ValidationError("Superuser cannot be a club member.\
            Please create a different account.")
