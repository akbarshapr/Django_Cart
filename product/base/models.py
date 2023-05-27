from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    img_url = models.CharField(max_length=2083)

    def __str__(self):
        return self.name


class Cart(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.IntegerField(default=1)

    @property
    def total_price(self):
        return self.item.price * self.quantity

    def __str__(self):
        return self.item.name
