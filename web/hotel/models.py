from account.validators import only_letters, alphanumeric
from base.models import TimeStampedModel
from django.contrib.auth.models import User
from django.core import validators
from django.db import models


class Hotel(TimeStampedModel):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='hotels')
    description = models.TextField(max_length=1000)
    country = models.CharField(max_length=150, validators=[only_letters])
    city = models.CharField(max_length=150, validators=[only_letters])
    street = models.CharField(max_length=100, validators=[alphanumeric])
    zip_code = models.CharField(max_length=10)
    is_wifi = models.BooleanField(default=False)
    is_pools = models.BooleanField(default=False)

    @property
    def full_address(self) -> str:
        return f'{self.street}, {self.zip_code} {self.city}'

    class Meta:
        ordering = ['-created_at']


class Room(TimeStampedModel):
    number = models.PositiveIntegerField(unique=True)
    beds = models.PositiveSmallIntegerField(default=1, validators=[
        validators.MinValueValidator(1),
        validators.MaxValueValidator(4)
    ])
    size = models.PositiveSmallIntegerField(validators=[
        validators.MinValueValidator(1),
        validators.MaxValueValidator(1000)
    ])
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_shower = models.BooleanField(default=True)
    is_tv = models.BooleanField(default=False)
    is_toilet = models.BooleanField(default=True)
    hotel = models.ForeignKey(to=Hotel, on_delete=models.CASCADE, related_name='rooms')

    class Meta:
        ordering = ['-created_at']
        unique_together = ['id', 'number']


class Comment(TimeStampedModel):
    content = models.TextField(max_length=1000)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='comments')
    hotel = models.ForeignKey(to=Hotel, on_delete=models.CASCADE, related_name='comments')
    rating = models.PositiveSmallIntegerField(default=5, validators=[
        validators.MinValueValidator(1),
        validators.MaxValueValidator(5),
    ])

    class Meta:
        ordering = ['-created_at']
