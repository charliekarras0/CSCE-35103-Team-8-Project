from django.db import models

# Create your models here.
class Player(models.Model):
    id = models.IntegerField(primary_key=True)
    codename = models.CharField(max_length=255)

    class Meta:
        db_table = 'players'