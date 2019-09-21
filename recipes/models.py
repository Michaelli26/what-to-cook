from django.db import models

# Create your models here.


class Recipe(models.Model):
    image = models.URLField()
    title = models.CharField(max_length=200)
    missing_count = models.IntegerField()
    source = models.URLField()

    def set_fields(self, hit, need):
        self.image = hit['recipe']['image']
        self.missing_count = need
        self.source = hit['recipe']['url']
        self.title = hit['recipe']['label']