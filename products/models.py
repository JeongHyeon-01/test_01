from django.db    import models

from cores.models import TimestampZone

class Category(TimestampZone): 
    name = models.CharField(max_length=45)

    class Meta: 
        db_table = 'categories'

class Product(TimestampZone): 
    name     = models.CharField(max_length=45)
    price    = models.DecimalField(max_digits=10,decimal_places=2)
    colors   = models.ManyToManyField('Color', through='productcolor')
    category = models.ForeignKey('Category', on_delete = models.CASCADE)

    class Meta: 
        db_table = 'products'

class Color(TimestampZone): 
    name = models.CharField(max_length=45)

    class Meta: 
        db_table = 'colors'

class Image(TimestampZone): 
    product_color = models.ForeignKey('ProductColor', on_delete=models.CASCADE)
    image_url     = models.CharField(max_length=3000)
    sequence      = models.IntegerField()

    class Meta: 
        db_table = 'images'

class ProductColor(TimestampZone): 
    product   = models.ForeignKey('Product', on_delete=models.CASCADE)
    color     = models.ForeignKey('Color', on_delete=models.CASCADE)
    inventory = models.IntegerField()

    class Meta: 
        db_table = 'productcolors'