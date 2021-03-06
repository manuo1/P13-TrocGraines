from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db import Error, models
from django.shortcuts import get_object_or_404
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from .text_constants import GLOBAL_ERROR_MSG, SEED_DELETED_MSG

user = get_user_model()


class SeedManager(models.Manager):
    """ manager for seed model """

    def get_last_seeds_added(self):
        """return last added seeds."""
        matching_list = []
        matching_list = Seed.objects.all().order_by(
            '-available', '-creation_date'
        )
        return matching_list

    def find_matching_seeds_to(self, searched_seed):
        """returns a list of objects corresponding to the searched words."""
        matching_list = []
        matching_list = (
            Seed.objects.annotate(search=SearchVector('name'))
            .filter(search=SearchQuery(searched_seed))
            .order_by('-available', 'name')
        )
        return matching_list

    def get_user_seeds(self, user):
        """returns a list of user seeds."""
        matching_list = []
        matching_list = Seed.objects.filter(owner=user).order_by(
            '-creation_date'
        )
        return matching_list

    def changes_seed_availability(self, seed_id):
        """ change the seed seed availability """
        messages = []
        seed = get_object_or_404(Seed, pk=seed_id)
        seed_old_state = seed.available
        seed.available = not seed_old_state
        try:
            seed.save()
        except Error:
            seed.available = seed_old_state
            messages.append({40: GLOBAL_ERROR_MSG})
        return messages

    def delete_seed(self, seed_id):
        """ delete a seed """
        messages = ''
        seed = get_object_or_404(Seed, pk=seed_id)
        try:
            seed_name = seed.name
            seed.delete()
            messages = [{40: SEED_DELETED_MSG.format(seed_name)}]
        except Error:
            messages = [{40: GLOBAL_ERROR_MSG}]
        return messages

    def get_seed(slef, seed_id):
        seed = get_object_or_404(Seed, pk=seed_id)
        return seed


class Seed(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()
    photo = ProcessedImageField(
        upload_to='images/',
        processors=[ResizeToFill(640, 360)],
        format='JPEG',
        options={'quality': 60},
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)
    owner = models.ForeignKey(user, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
