from django.db   import models

from core.models import TimeStampModel

class Item(TimeStampModel):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    image = models.ImageField(upload_to='img/')

    class Meta:
        db_table = 'items'

    def __str__(self):
        return self.name