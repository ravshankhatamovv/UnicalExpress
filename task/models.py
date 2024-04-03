from django.db import models
from django.utils.html import mark_safe
# Create your models here.


class Shop(models.Model):
    title=models.CharField(max_length=20)
    description=models.CharField(max_length=200)
    image=models.ImageField(upload_to='images/')
    product=models.ForeignKey('Product', on_delete=models.CASCADE, related_name='shop')

    class Meta:
        permissions=[("change_shop_features","change things related to Shop"),]

    def __str__(self):
        return f"{self.title}"
    
    def get_image_url(self):
        """
        this method for retrieving absolute url of the image
        """
        return self.image.url
    
    def photo(self): 
        """
        this method responsible for providing the image of shop at admin panel
        """
        return mark_safe(f'<img src = "{self.image.url}" width = "50"/>')

class Category(models.Model):
    title=models.CharField(max_length=20, blank=True)
    description=models.CharField(max_length=200, blank=True)
    parents = models.ForeignKey('self',on_delete=models.CASCADE,related_name='sub_category',blank=True,)


    class Meta:
        verbose_name='Categories'
        verbose_name_plural='Categories'
        permissions = [("change_category_features","change things related to Category"),]

    def __str__(self):
        return f"{self.title}"
    
    

class ProductImage(models.Model):
    image_name=models.CharField(max_length=25, blank=True)
    image=models.ImageField(upload_to="images/", blank=True)

    class Meta:
        permissions=[("change_image_of_product_features","change things related to ProductImage"),]

    def __str__(self):
        return f"{self.image_name}"
    
    def img_preview(self): 
        """
        responsible for providing the image for the model at admin panel
        """
        return mark_safe(f'<img src = "{self.image.url}" width = "50"/>')
    
    @property
    def get_image_url(self):
        """
        for retrieving absolute url of the image
        """
        return self.image.url

class Product(models.Model):
    category=models.ManyToManyField(to=Category, related_name='product_category')
    description=models.CharField(max_length=200, blank=True)
    title=models.CharField(max_length=20, blank=True)
    amount=models.IntegerField()
    price=models.FloatField()
    active=models.BooleanField(blank=True)
    product_image=models.ManyToManyField(ProductImage, related_name="product")

    class Meta:
        permissions=[("change_product_features","change things related to Product"),]

    def __str__(self) -> str:
        return f"{self.title}"
            
    @property
    def image_url(self):
        """
        filter images and retrieve first one's image url
        """
        image=self.product_image.filter(id=self.id).first()
        return image.get_image_url
    
    def photo(self):
        """
        is for provide image for product at admin panel
        """
        return mark_safe(f'<img src = "{self.image_url}" width = "50"/>')