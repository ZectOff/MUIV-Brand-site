from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from goods.forms import ProductReviewForm
from goods.models import ProductReview, Products
from goods.product_media import get_product_gallery_images
from goods.services import (
    get_product_rating_stats,
    get_product_reviews,
    get_user_favorite_products,
    is_product_favorite,
    toggle_product_favorite,
    user_can_add_review,
    user_has_purchased_product,
)
from goods.utils import q_search


def catalog(request, category_slug=None):

    page = request.GET.get('page', 1)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)

    if query:
        goods = q_search(query)
    elif category_slug == "vse-tovary":
        goods = Products.objects.all()
    else:
        goods = Products.objects.filter(category__slug=category_slug)
        if not goods.exists():
            raise Http404

    if on_sale:
        goods = goods.filter(discount__gt=0)

    if order_by and order_by != "default":
        goods = goods.order_by(order_by)

    paginator = Paginator(goods, 12)
    current_page = paginator.page(int(page))

    context = {
        'title': 'Категории',
        'products': current_page,
        'slug_url': category_slug
    }
    return render(request, 'goods/catalog.html', context)


def _handle_review_post(request, product):
    if not request.user.is_authenticated:
        login_url = reverse('user:login')
        return redirect(f'{login_url}?next={request.path}')

    if not user_has_purchased_product(request.user, product):
        messages.error(
            request,
            'Отзыв могут оставить только те, кто уже заказал этот товар.',
        )
        return redirect(request.path)

    if ProductReview.objects.filter(user=request.user, product=product).exists():
        messages.warning(request, 'Вы уже оставили отзыв на этот товар.')
        return redirect(request.path)

    form = ProductReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.product = product
        review.save()
        messages.success(request, 'Спасибо! Ваш отзыв опубликован.')
        return redirect(request.path)

    return form


def product(request, product_slug):
    product_obj = get_object_or_404(
        Products.objects.select_related('category').prefetch_related('additional_images'),
        slug=product_slug,
    )
    review_form = ProductReviewForm()

    if request.method == 'POST' and request.POST.get('review_submit'):
        result = _handle_review_post(request, product_obj)
        if isinstance(result, ProductReviewForm):
            review_form = result
        elif result is not None:
            return result

    user_review = None
    can_review = False
    if request.user.is_authenticated:
        user_review = ProductReview.objects.filter(
            user=request.user,
            product=product_obj,
        ).first()
        can_review = user_can_add_review(request.user, product_obj)

    gallery_images = get_product_gallery_images(product_obj)
    is_favorite = is_product_favorite(request.user, product_obj)

    prd_data = {
        'title': 'MUIV Brand - Карта товара ',
        'catgoods': ['Img-1', 'Img-2', 'Img-3',],
        'product': product_obj,
        'gallery_images': gallery_images,
        'reviews': get_product_reviews(product_obj),
        'rating_stats': get_product_rating_stats(product_obj),
        'review_form': review_form,
        'user_review': user_review,
        'can_review': can_review,
        'has_purchased': user_has_purchased_product(request.user, product_obj),
        'is_favorite': is_favorite,
    }
    return render(request, 'goods/product.html', context=prd_data)


@login_required
def favorites(request):
    products = get_user_favorite_products(request.user)
    context = {
        'title': 'MUIV Brand — Избранное',
        'products': products,
    }
    return render(request, 'goods/favorites.html', context)


@login_required
def favorite_toggle(request):
    if request.method != 'POST':
        return JsonResponse({'message': 'Метод не поддерживается'}, status=405)

    product_id = request.POST.get('product_id')
    if not product_id:
        return JsonResponse({'message': 'Не указан товар'}, status=400)

    product_obj = get_object_or_404(Products, id=product_id)
    is_favorite = toggle_product_favorite(request.user, product_obj)

    return JsonResponse({
        'is_favorite': is_favorite,
        'message': 'Добавлено в избранное' if is_favorite else 'Удалено из избранного',
    })
