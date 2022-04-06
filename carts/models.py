from django.db    import models

from cores.models import TimestampZone

class Cart(TimestampZone): 
    user     = models.ForeignKey('users.user', on_delete=models.CASCADE)
    product  = models.ForeignKey('products.product', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def total_price(self): 
        return self.quantity * self.product.price

    class Meta: 
        db_table = 'carts'