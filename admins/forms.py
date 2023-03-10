from django import forms
from tinymce.widgets import TinyMCE

from store.models import Product


class ProductForm(forms.ModelForm):
    ...
    description = forms.CharField(
        widget=TinyMCE(attrs={'rows': 30, 'cols': 20, 'data-parsley-validate'
                                                      '-field': 5}))
    ...

    class Meta:
        model = Product
        fields = [
            'description',
        ]
