from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
# from django.contrib.auth import get_user_model
#
# User = get_user_model()

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(User, related_name='product', default=1, null=False, on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

    def get_average_rating(self):
        ratings = [rating.value for rating in self.ratings.all()]
        if ratings:
            return sum(ratings) / len(ratings)
        return 0


class Chat(models.Model):
    product_id = models.ForeignKey(Product, related_name='chat', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, related_name='chat', on_delete=models.CASCADE)
    message = models.TextField()
    time_sent = models.DateTimeField()

    def __str__(self):
        return "Product_ID:" + str(self.product_id) + " USER_ID:" + str(self.user_id)


class Watchlist(models.Model):
    user_id = models.ForeignKey(User, related_name='watches', on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, related_name='watches', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "USER_ID:" + str(self.user_id) + " Product_ID:" + str(self.product_id)


class Likelist(models.Model):
    user_id = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, related_name='likes', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "USER_ID:" + str(self.user_id) + " Product_ID:" + str(self.product_id)


class Rating(models.Model):
    user_id = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, related_name='ratings', on_delete=models.CASCADE)
    value = models.IntegerField(choices=[(1,1), (2,2), (3,3), (4,4), (5,5)])

    def __str__(self):
        return "USER_ID:" + str(self.user_id) + " Product_ID:" + str(self.product_id)
