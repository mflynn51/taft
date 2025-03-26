class DeleteLocationForm(forms.Form):
    location = forms.ModelChoiceField(
        queryset=GeoPoint.objects.all(),
        empty_label="Pick a diverion point to delete",
        widget=forms.Select(attrs={'class': 'form-control'})
    )