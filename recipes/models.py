from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Recipe(models.Model):
    image = models.URLField()
    title = models.CharField(max_length=200)
    missing_count = models.IntegerField(null=True, blank=True)
    source = models.URLField()
    users = models.ManyToManyField(User)

    def set_fields(self, hit, need):
        self.image = hit['recipe']['image']
        self.missing_count = need
        self.source = hit['recipe']['url']
        self.title = hit['recipe']['label']

    def save_model(self, account):
        self.users.add(account)
        self.save()
