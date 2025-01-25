from django import forms
from .models import WasteImage

class WasteImageForm(forms.ModelForm):
    class Meta:
        model = WasteImage
        fields = ['image', 'description']
        
# Forms

class WasteReportForm(forms.Form):
    description = forms.CharField(max_length=255, widget=forms.Textarea)
    location = forms.CharField(max_length=255)
    waste_type = forms.ChoiceField(choices=[('Organic', 'Organic'), ('Plastic', 'Plastic'), ('Other', 'Other')])
    file = forms.FileField(required=False)
