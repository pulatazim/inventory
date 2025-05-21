from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=250)
    code = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class ProductMaterial(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.FloatField()

    class Meta:
        unique_together = ('product', 'material')

    def __str__(self):
        return f"{self.product.name} - {self.material.name} - {self.quantity}"


class Warehouse(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    remainder = models.FloatField()
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.material.name} - {self.remainder} left"