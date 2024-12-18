from django import forms
from product.models import Product


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("name", "description", "price", "logo")

    def save(self, commit=True, store=None):
        product = super().save(commit=False)
        if store:
            product.store_id = store
        if commit:
            product.save()
        return product

class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("name", "description", "price", "logo")