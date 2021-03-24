from django.contrib.postgres.search import SearchQuery, SearchVector
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

user = get_user_model()

class SeedManager(models.Manager):

    def get_last_seeds_added(self):
        """ return last added seeds """
        matching_list = []
        matching_list = Seed.objects.order_by('-creation_date').all()
        return matching_list

    def find_matching_seeds_to(self, searched_seed):
        """returns a list of objects corresponding to the searched words."""
        matching_list = []
        matching_list = (
            Seed.objects.annotate(search=SearchVector('name'))
            .filter(search=SearchQuery(searched_seed))
            .order_by('name')
        )
        return matching_list

    def get_user_seeds(self, owner):
        """returns a list of user seeds."""
        matching_list = []
        matching_list = (
            Seed.objects.annotate(search=SearchVector('owner'))
            .filter(search=SearchQuery(searched_seed))
            .order_by('name')
        )
        return matching_list


class Seed(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()
    photo = ProcessedImageField(upload_to='images/',
                                   processors=[ResizeToFill(800, 600)],
                                   format='JPEG',
                                   options={'quality': 60})
    creation_date = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)
    owner = models.ForeignKey(user, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
