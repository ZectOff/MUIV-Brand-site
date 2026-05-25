from django import forms

from goods.models import ProductReview


class ProductReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        label='Оценка',
    )

    class Meta:
        model = ProductReview
        fields = ('rating', 'text')
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'class': 'product-review-text',
                    'rows': 3,
                    'placeholder': 'Расскажите о товаре…',
                }
            ),
        }
        labels = {
            'text': 'Отзыв',
        }
