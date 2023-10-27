from django.db              import models

from core.models            import TimeStampModel

class Item(TimeStampModel):
    category   = models.ForeignKey('Category', on_delete=models.CASCADE)
    name       = models.CharField(max_length=200)
    price      = models.FloatField()
    quantity   = models.PositiveSmallIntegerField()
    image_url  = models.URLField(max_length=400, blank=True)

    class Meta:
        db_table = 'items'

    def __str__(self):
        return self.name

class Category(models.Model):
    name      = models.CharField(max_length=100)
    thumbnail = models.URLField(max_length=400, blank=True)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name