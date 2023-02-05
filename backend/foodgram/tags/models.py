from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
