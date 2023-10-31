from django.db    import models

from users.models import User
from items.models import Item
from core.models  import TimeStampModel

class Cart(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'carts'

    def __str__(self):
        return self.item