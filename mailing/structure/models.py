from django.db import models


class Note(models.Model):
    id = models.IntegerField(primary_key=True)
    number = models.IntegerField(unique=True)
    text = models.TextField(blank=True)
    crypto_text = models.TextField()

    def __repr__(self):
        return f'Notes number: {self.number}'

    class Meta:
        verbose_name = 'notes'

