from django import forms

from .models import Watch


class WatchForm(forms.ModelForm):
    class Meta:
        model = Watch
        fields = [
            "name",
            "brand",
            "category",
            "movement_type",
            "price",
            "purchase_date",
            "is_in_collection",
            "description",
            "tags",
        ]
        widgets = {
            "purchase_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_price(self):
        price = self.cleaned_data["price"]

        if price < 0:
            raise forms.ValidationError("Price cannot be negative.")

        return price

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if len(name) < 2:
            raise forms.ValidationError(
                "Watch name must contain at least 2 characters."
            )

        return name
