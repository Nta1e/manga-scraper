from django.db import models


class Manga(models.Model):
    title = models.CharField(max_length=255, blank=False)
    image = models.URLField()
    description = models.TextField()


class Chapters(models.Model):
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    number = models.IntegerField()
    image = models.URLField()


class Pages(models.Model):
    page_number = models.IntegerField()
    chapter = models.ForeignKey(Chapters, on_delete=models.CASCADE)
    image = models.URLField()
