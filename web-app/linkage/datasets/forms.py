import logging
from django.forms import ModelForm, Textarea, TextInput, Select, ChoiceField, HiddenInput
from django.utils.translation import ugettext_lazy as _

from .models import Dataset

logger = logging.getLogger(__name__)


class DatasetForm(ModelForm):
    class Meta:
        model = Dataset
        fields = ['name', 'description', 'format', 'url']

        labels = {
            'name': _('Dataset Name'),
            'description': _('Description'),
            'format': _('File Format'),
            'url': _('File Name'),
        }
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'format': Select(attrs={'class': 'form-control'}),
            'url': TextInput(attrs={'class': 'form-control'}),
        }


class DatasetUpdateForm(DatasetForm):

    class Meta(DatasetForm.Meta):

        fields = DatasetForm.Meta.fields + ['data_types', 'field_cats']

    def __init__(self, *args, **kwargs):
        super(DatasetUpdateForm, self).__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['data_types'].widget = HiddenInput()
            self.fields['field_cats'].widget = HiddenInput()


