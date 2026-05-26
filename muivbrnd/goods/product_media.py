CATEGORY_PLACEHOLDER_ICONS = {
    'odezhda': 'deps/img/category-icons/odezhda.png',
    'aksessuary': 'deps/img/category-icons/aksessuary.png',
    'kancelyariya': 'deps/img/category-icons/kancelyariya.png',
}

DEFAULT_PLACEHOLDER_ICON = CATEGORY_PLACEHOLDER_ICONS['kancelyariya']


def category_placeholder_icon(category) -> str:
    if category is None:
        return DEFAULT_PLACEHOLDER_ICON
    slug = getattr(category, 'slug', None) or ''
    return CATEGORY_PLACEHOLDER_ICONS.get(slug, DEFAULT_PLACEHOLDER_ICON)


def product_has_image(product) -> bool:
    image = getattr(product, 'image', None)
    if not image or not image.name:
        return False
    try:
        return image.storage.exists(image.name)
    except Exception:
        return False


def image_field_url(image_field):
    if not image_field or not getattr(image_field, 'name', None):
        return None
    try:
        if not image_field.storage.exists(image_field.name):
            return None
        return image_field.url
    except Exception:
        return None


def get_product_gallery_images(product):
    gallery = []

    main_image_url = image_field_url(getattr(product, 'image', None))
    if main_image_url:
        gallery.append({
            'url': main_image_url,
            'alt': product.name,
        })

    additional_images = getattr(product, 'additional_images', None)
    if additional_images is None:
        return gallery

    for item in additional_images.all():
        image_url = image_field_url(item.image)
        if not image_url:
            continue
        gallery.append({
            'url': image_url,
            'alt': item.title or product.name,
        })

    return gallery
