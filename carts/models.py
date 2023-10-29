from django.db    import models

from users.models import User
from items.models import Item
from core.models  import TimeStampModel

class Cart(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'carts'

    def sub_total(self):
        return self.item.price * self.quantity

    def __str__(self):
        return self.item