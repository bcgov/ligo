import logging
from django.forms import ModelForm, Textarea, TextInput, Select, ChoiceField, HiddenInput
from django.utils.translation import ugettext_lazy as _

from .models import Dataset

logger = logging.getLogger(__name__)


class DatasetForm(ModelForm):
    class Meta:
        model = Dataset
        fields = ['name', 'title', 'description', 'format', 'url']

        labels = {
            'name': _('Dataset Name'),
            'title': _('Title'),
            'description': _('Description'),
            'format': _('File Format'),
            'url': _('File Name'),
        }
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'format': Select(attrs={'class': 'form-control'}),
            'url': TextInput(attrs={'class': 'form-control'}),
        }


class DatasetUpdateForm(DatasetForm):

    class Meta(DatasetForm.Meta):

        fields = DatasetForm.Meta.fields + ['index_field', 'entity_field', 'data_types', 'field_cats']

    def __init__(self, *args, **kwargs):
        super(DatasetUpdateForm, self).__init__(*args, **kwargs)

        # Get the list of dataset columns to fill index_field select box
        if self.instance.pk:
            try:
                data = Dataset.objects.get(pk=self.instance.pk)
                columns = [(item, item) for item in data.get_fields()]

                self.fields['index_field'] = ChoiceField(
                    choices=columns,
                    label='Index Field',
                    widget=Select(attrs={'class': 'form-control'}))

                self.fields['entity_field'] = ChoiceField(
                    choices=columns,
                    label='Entity Identifier Field',
                    widget=Select(attrs={'class': 'form-control'}))

                self.fields['data_types'].widget = HiddenInput()
                self.fields['field_cats'].widget = HiddenInput()

            except Dataset.DoesNotExist:
                logger.error('Database error: No dataset with id {0} was found.'.format(self.instance.pk))
                pass


