from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Material, ProductMaterial, Warehouse
from .serializers import ProductRequestSerializer


class MaterialCalculationApiView(APIView):

    def post(self, request):
        serializer = ProductRequestSerializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product_data = serializer.validated_data
        warehouse_usage = {}  # # {warehouse_id: used_qty}
        result = []     # Yakuniy natijani yigamiz

        for product_item in product_data:
            product_code = product_item["product_code"]
            product_qty = product_item["quantity"]

            try:
                product = Product.objects.get(code=product_code)
            except Product.DoesNotExist:
                return Response({'error': f'Product with code {product_code} not found'},
                                status=status.HTTP_404_NOT_FOUND)

            product_result = {
                "product_name": product.name,
                "product_qty": product_qty,
                "product_materials": []
            }

            product_materials = ProductMaterial.objects.filter(product=product)

            for pm in product_materials:
                material = pm.material
                total_needed = product_qty * pm.quantity
                allocated_qty = 0

                warehouses = Warehouse.objects.filter(material=material).order_by('created_at')

                for wh in warehouses:
                    key = (material.id, wh.id)
                    already_taken = warehouse_usage.get(key, 0)
                    available = wh.remainder - already_taken

                    if available <= 0:
                        continue  # Bu omborda bu material qolmagan

                    to_take = min(total_needed - allocated_qty, available)
                    allocated_qty += to_take
                    warehouse_usage[key] = already_taken + to_take

                    product_result["product_materials"].append({
                        "warehouse_id": wh.id,
                        "material_name": material.name,
                        "qty": to_take,
                        "price": wh.price
                    })

                    if allocated_qty == total_needed:
                        break

                if allocated_qty < total_needed:
                    # Yetmayotgan qism
                    product_result["product_materials"].append({
                        "warehouse_id": None,
                        "material_name": material.name,
                        "qty": total_needed - allocated_qty,
                        "price": None
                    })

            result.append(product_result)

        return Response({"result": result})
