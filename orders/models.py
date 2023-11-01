from django.db   import models

from core.models import TimeStampModel

class Order(TimeStampModel):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    address = models.CharField(max_length=500)
    order_number = models.CharField(max_length=150, unique=True)
    order_status = models.ForeignKey('OrderStatus', on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return self.order_number

class OrderStatus(models.Model):
    status = models.CharField(max_length=10)

    class Status(models.IntegerChoices):
        PENDING   = 1
        COMPLETED = 2
        DECLINED  = 3

    class Meta:
        db_table = 'order_status'