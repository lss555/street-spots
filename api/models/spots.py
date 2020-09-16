from django.db import models
from django.contrib.auth import get_user_model

class Spot(models.Model):
  country = models.CharField(max_length=60)
  state = models.CharField(max_length=30)
  city = models.CharField(max_length=100)
  description = models.TextField()
  owner = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE
    )
  SEASON_CHOICES = [
    ('Summer', 'Summer'),
    ('Winter', 'Winter'),
    ('Either', 'Either'),
  ]
  season = models.CharField(max_length=50, blank=True, null=True, choices=SEASON_CHOICES)

  def __str__(self):
    return f"Your ski spots info: country: '{self.country}' state: '{self.state}' season: '{self.season}' description: '{self.description}' city: '{self.city}'"

  def as_dict(self):
    """ returns dictionary version of spot models """
    return {
      'id': self.id,
      'country': self.country,
      'state': self.state,
      'city': self.city,
      'description': self.description,
      'season': self.season
    }
