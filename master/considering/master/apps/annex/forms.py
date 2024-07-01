from apps.annex.models import Annex
from django.forms import ModelForm


class AnnexForm(ModelForm):
    class Meta:
        model = Annex
        fields = [
            'file',
            'raw_name',
            # 'detail'
        ]
