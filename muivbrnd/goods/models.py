from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.conf import settings

import math
import locale

from django.urls import reverse


class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'category'
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='goods_images', blank=True, null=True, verbose_name='Изображение')
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, verbose_name='Скидка в %')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Категория')

    class Meta:
        db_table = 'product'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ("id",)
    
    def __str__(self):
        return f'{self.name} Количество - {self.quantity}'
    
    def get_absolute_url(self):
        return reverse("catalog:product", kwargs={"product_slug": self.slug})
    
    def display_id(self):
        return f'{self.id:05}'
    
    def sell_price(self):
        if self.discount:
            disc_value = math.floor(round(self.price - self.price*self.discount/100, 2))
            locale.setlocale(locale.LC_ALL, '')
            result = float("{:.2f}".format(disc_value))
            locale.str(result)
            return result
        
        return self.price
    
    def self_discount_int(self):
        return int(self.discount)


class ProductReview(models.Model):
    product = models.ForeignKey(
        to=Products,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Товар',
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='product_reviews',
        verbose_name='Пользователь',
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Оценка',
    )
    text = models.TextField(verbose_name='Текст отзыва')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        db_table = 'product_review'
        verbose_name = 'Отзыв о товаре'
        verbose_name_plural = 'Отзывы о товарах'
        ordering = ('-created_at',)
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'product'),
                name='unique_user_product_review',
            ),
        ]

    def __str__(self):
        return f'{self.product.name} — {self.user} ({self.rating})'