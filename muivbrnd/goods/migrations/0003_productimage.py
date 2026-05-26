from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('goods', '0002_product_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='goods_images', verbose_name='Изображение')),
                ('title', models.CharField(blank=True, help_text='Необязательно. Короткое описание/подпись изображения.', max_length=150, null=True, verbose_name='Подпись')),
                ('sort_order', models.PositiveSmallIntegerField(default=0, help_text='Чем меньше число, тем раньше картинка в галерее.', verbose_name='Порядок')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additional_images', to='goods.products', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Изображение товара',
                'verbose_name_plural': 'Изображения товара',
                'db_table': 'product_image',
                'ordering': ('sort_order', 'id'),
            },
        ),
    ]
