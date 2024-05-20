import random
import string
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator



class Category(models.Model):
    name = models.CharField(max_length=250,db_index = True, verbose_name='Категория')
    parent = models.ForeignKey(to='self',on_delete=models.CASCADE,related_name='children',blank=True,null=True , verbose_name='Родительская катагория')
    slug = models.SlugField(verbose_name = 'URL',max_length=250 ,unique=True,null=False,editable=True)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Дата создания')

    class Meta:
        unique_together = (['slug' , 'parent'])
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    @staticmethod
    def _rand_slug():
        """
        Generates a random slug consisting of lowercase letters and digits.
        Example:
            >>> rand_slug()
            'abc123'
        """
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k=k.parent
        return ' > '.join(full_path[::-1])
    
    def save(self,*args,**kwargs):
        
        if not self.slug:
            self.slug = slugify(self._rand_slug() + '-PickBetter' + self.name)
        super(Category,self).save(*args , **kwargs)


    def get_absolute_url(self):
        return reverse("shop:category-list", args = [str(self.slug)])


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField("Название", max_length=250)
    brand = models.CharField("Бренд", max_length=250)
    description = models.TextField("Описание", blank=True)
    slug = models.SlugField('URL', max_length=250)
    price = models.DecimalField("Цена", max_digits=7, decimal_places=2, default=99.99)
    image = models.ImageField("Изображение", upload_to='images/products/%Y/%m/%d',blank=True,null=True,default='products/products/def.jpg')
    available = models.BooleanField("Наличие", default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True , db_index=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True)
    discount = models.IntegerField(default=0,blank=True,null=True,validators=[MinValueValidator(0),MaxValueValidator(100)])

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("shop:product-detail", args=[str(self.slug)])
    

    def get_discounted_price(self):
        return round(self.price - (self.price * self.discount / 100))
    
    @property
    def full_image_url(self):
        return self.image.url if self.image else ''



class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager , self).get_queryset().filter(available=True)



class ProductProxy(Product):

    objects = ProductManager()

    class Meta:
        proxy=True

    