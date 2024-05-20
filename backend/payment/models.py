from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from shop.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class ShippingAddress(models.Model):
    full_name = models.CharField(max_length=250)
    email = models.EmailField(verbose_name='email_address',max_length=254)
    street_address = models.CharField(max_length=250)
    apartment_address = models.CharField(max_length=250)
    country = models.CharField(max_length = 100,blank=True,null=True)
    zip_code = models.CharField(max_length=100,blank=True,null=True)
    city = models.CharField(max_length=250,blank=True,null=True)

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'
        ordering = ['id']

    def __str__(self):
        return f'{self.full_name} - {self.email}'
    
    def get_absolute_url(self):
        return f'/payment/shipping' 
    

    @classmethod
    def create_default_shipping_address(cls, user):
        default_shipping_address = {'user':user , 'full_name':'No name' , 'email': 'example@mail.com','street_address': 'Fill Address','apartment_address':'Fill Address','country':''}
        shipping_address = cls(**default_shipping_address)
        shipping_address.save()
        return shipping_address    



class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE , blank=True,null=True)

    shipping_address = models.ForeignKey(ShippingAddress,on_delete=models.CASCADE , blank=True,null=True)

    amount = models.DecimalField(max_digits=9 , decimal_places=2)

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    paid = models.BooleanField(default=False)
    
    discount = models.IntegerField(default=0,blank=True,null=True,validators=[MinValueValidator(0),MaxValueValidator(100)])



    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(amount__gte=0), name='amount_gte_0'),
        ]

    def __str__(self):
        return f'{self.user} - {self.amount}'
    
    def get_absolute_url(self):
        return reverse("payment:order_detail", kwargs={"pk": self.pk})

    def get_total_cost_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())

    @property
    def get_discount(self):
        if (total_cost := self.get_total_cost_before_discount()) and self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)

    def get_total_cost(self):
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount
    

class OrderItem(models.Model):

    order = models.ForeignKey(Order,on_delete=models.CASCADE , blank=True,null=True , related_name='items')

    quantity = models.IntegerField(default=1)

    product = models.ForeignKey(Product , on_delete=models.CASCADE , blank=True,null=True)

    user = models.ForeignKey(User,on_delete=models.CASCADE , blank=True,null=True)

    price = models.DecimalField(max_digits=9 , decimal_places=2)


    class Meta:
        verbose_name = "OrderItem"
        verbose_name_plural = "OrderItems"
        ordering = ['-id']
        constraints = [
            models.CheckConstraint(check=models.Q(
                quantity__gt=0), name='quantity_gte_0'),
        ]


    
    
    def __str__(self):
        return f'{self.user} - {self.price}'
    

    def get_cost(self):
        return self.price * self.quantity

    @property
    def total_cost(self):
        return self.price * self.quantity

    @classmethod
    def get_total_quantity_for_product(cls, product):
        return cls.objects.filter(product=product).aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0

    @staticmethod
    def get_average_price():
        return OrderItem.objects.aggregate(average_price=models.Avg('price'))['average_price']





