from django import forms
from store.models import Store


class CreateStoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ("name", "description", "logo")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        store = super().save(commit=False)
        store.owner = self.user
        if commit:
            store.save()
        return store
