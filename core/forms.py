from django import forms
from .models import *

class WaterQualityIndexForm(forms.ModelForm):
	class Meta:
		model = WaterQualityIndex
		exclude = ('wqi','level')