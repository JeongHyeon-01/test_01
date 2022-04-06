import json

from django.http import JsonResponse
from django.views import View
from carts.models import Cart
from products.models import ProductColor, Image
from cores.decorator import login_auchorization
from django.forms   import ValidationError
from carts.validator import validate_quantity,validate_total_quantity


class CartView(View):
    @login_auchorization
    def post(self, request):
        # try:
            data = json.loads(request.body)
            user = request.body
            quantity = abs(data['quantity',1])
            product_id = ProductColor.objects.get(id=data['product'])
            inventory = product_id.inventory
            
            cart, is_created = Cart.objects.get_or_create(
                user = user ,
                product_color = product_id,
                default = {'quantity': 0}
            )
            cart.quantity += quantity
            cart.save()
            
            if is_created:
                return JsonResponse(status=200)
            else:
                return JsonResponse(status=200)

        # except ProductColor.DoesNotExist:
        #     return JsonResponse({'message' : 'Product does not exist'}, status=400)

        # except KeyError:
        #     return JsonResponse({'message' : 'Key error'}, status=400)

        # except ValidationError as e:
        #     return JsonResponse({'message' : e.message}, status=400)