from django.contrib import admin

from goods.models import Categories, ProductFavorite, ProductImage, ProductReview, Products

# admin.site.register(Categories)
# admin.site.register(Products)


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    class ProductImageInline(admin.TabularInline):
        model = ProductImage
        extra = 1
        fields = ('image', 'title', 'sort_order')
        ordering = ('sort_order', 'id')

    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "quantity", "price", "discount"]
    list_editable = ["discount"]
    search_fields = ["name", "description"]
    list_filter = ["discount", "quantity", "category"]
    inlines = (ProductImageInline,)
    fields = [
        "name",
        "category",
        "slug",
        "description",
        "image",
        ("price", "discount"),
        "quantity",
    ]


@admin.register(ProductFavorite)
class ProductFavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
    list_filter = ('created_at', 'product__category')
    search_fields = ('user__username', 'product__name')
    raw_id_fields = ('user', 'product')
    readonly_fields = ('created_at',)


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'product__category')
    search_fields = ('product__name', 'user__username', 'text')
    readonly_fields = ('created_at',)
    raw_id_fields = ('product', 'user')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'sort_order', 'title', 'created_at')
    list_filter = ('product__category', 'created_at')
    search_fields = ('product__name', 'title')
    raw_id_fields = ('product',)
