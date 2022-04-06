from django.db.models       import Q
from django.http            import JsonResponse
from django.views           import View

from products.models import *

class ProductListView(View): 
    def get(self, request):
        offset      = int(request.GET.get('offset', 0))
        limit       = int(request.GET.get('limit', 100))
        
        products = Product.objects.all()[offset:limit+offset]
        
        result=[{ 
            "category"  : Category.objects.get(id=product.category_id).id,
            "product_id": product.id,
            "name"      : product.name,
            "price"     : product.price,
            "colors"  : [{
                "primary_key": color.id,
                "color_id"   : color.color.id,
                "color"      : color.color.name,
                "image": [image.image_url for image in Image.objects.filter(product_color_id=color.id, sequence=1)][0]
            }for color in ProductColor.objects.filter(product_id = product.id)]
        }for product in products]
    
        return JsonResponse({"result":result}, status=200)

class DetailView(View): 
    def get(self, request, product_id): 
        color        = request.GET.get('color', None)
        product_data = ProductColor.objects.filter(product_id=product_id)
        
        if color != None:
            product_data = ProductColor.objects.filter(product_id=product_id, color_id=color)

        result=[{
            "name"      : product.product.name,
            "price"     : product.product.price,
            "result"    : [{
                "primary_key": product.id,
                "color"      : product.color.name,
                "image_list" : [image.image_url for image in Image.objects.filter(product_color_id = product.color.id)]
            }]
        }for product in product_data]
        
        return JsonResponse({"result" : result}, status=200)

class SmartSearchView(View): 
    def bulid(self, qs):
        categories = qs.GET.getlist('category', None)
        colors     = qs.GET.getlist('color',None)
        product    = qs.GET.get('product',None)
        max_price  = qs.GET.get('max_price',100000000)
        min_price  = qs.GET.get('min_price',0)
    
        q = Q(product__price__range = (min_price, max_price))

        if categories:
            q &= Q(product__category_id__in = categories)

        if product:
            q &= Q(product__name__icontains = product)
                       
        if colors:
            q &= Q(color__name__in = colors)

        return q

    def get(self, request): 

        q = self.bulid(qs=request)

        products = ProductColor.objects.filter(q)

        result=[{
            "primary_key"  : product.id,
            "category_name"     : product.product.category.name,
            "product_name" : product.product.name,
            "color_name"   : product.color.name,
            "product_price": product.product.price,
            "image_url"        : Image.objects.get(product_color_id = product.id, sequence=1).image_url
        }for product in products]
     
        return JsonResponse({"result":result}, status=200)