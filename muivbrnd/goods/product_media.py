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
