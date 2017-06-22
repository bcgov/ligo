import json
import logging
from django import forms
from django.forms.models import inlineformset_factory
from django.forms import (ModelForm,
                          CharField,
                          Textarea,
                          TextInput,
                          Select,
                          ModelChoiceField,
                          HiddenInput,
                          ChoiceField,
                          CheckboxInput)

from django.utils.translation import ugettext_lazy as _

from .models import LinkingProject, LinkingStep, PROJECT_TYPES
from linkage.datasets.models import Dataset

logger = logging.getLogger(__name__)

TYPE_CHOICES = (('', 'Select Project Type'),) + PROJECT_TYPES


class ProjectTypeForm(forms.Form):
    type = ChoiceField(
        label='Project Type',
        choices=TYPE_CHOICES,
        widget=Select(attrs={'class': 'form-control'}))


class ProjectForm(ModelForm):
    left_data = ModelChoiceField(queryset=Dataset.objects.all(), label='Left',
                                 widget=Select(attrs={'class': 'form-control'}))
    left_columns = CharField(widget=HiddenInput(), required=False)

    class Meta:
        model = LinkingProject
        fields = ['name', 'description', 'status']

        labels = {
            'name': _('Project Name'),
            'description': _('Description')
        }
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'status': HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['left_data'].queryset = Dataset.objects.all()

        if self.instance.pk:
            try:
                data = LinkingProject.objects.get(pk=self.instance.pk)
                left_dataset = data.linkingdataset_set.get(link_seq=1)
                self.fields['left_data'].initial = left_dataset.dataset.pk
                try:
                    columns = json.loads(left_dataset.columns) or []
                except json.JSONDecodeError as json_err:
                    logger.error('Error on parsing json data of dataset columns.')
                    columns = []
                if left_dataset.dataset.index_field is not None and left_dataset.dataset.index_field not in columns:
                    columns.append(left_dataset.dataset.index_field)
                if left_dataset.dataset.entity_field is not None and left_dataset.dataset.entity_field not in columns:
                    columns.append(left_dataset.dataset.entity_field)
                self.fields['left_columns'].initial = columns

            except LinkingProject.DoesNotExist as project_err:
                logger.error('Database error. Linking project with id {0} was not found'.format(self.instance.pk))
            except Exception as db_err:
                logger.error('Database error on fetching Linking project with id {0}.'.format(self.instance.pk))
                pass


class LinkingForm(ProjectForm):
    right_data = ModelChoiceField(queryset=Dataset.objects.all(), label='right',
                                  widget=Select(attrs={'class': 'form-control'}))
    right_columns = CharField(widget=HiddenInput(), required=False)


    class Meta(ProjectForm.Meta):
        fields = ProjectForm.Meta.fields + ['relationship_type']

        labels = ProjectForm.Meta.labels
        labels['relationship_type'] = _('Entity Relationship Type')

        widgets = ProjectForm.Meta.widgets
        widgets['relationship_type'] = Select(attrs={'class': 'form-control'})

    def __init__(self, *args, **kwargs):
        super(LinkingForm, self).__init__(*args, **kwargs)
        self.fields['right_data'].queryset = Dataset.objects.all()

        # Get the list of dataset columns to fill index_field select box
        if self.instance.pk:
            try:
                data = LinkingProject.objects.get(pk=self.instance.pk)
                right_dataset = data.linkingdataset_set.get(link_seq=2)
                self.fields['right_data'].initial = right_dataset.dataset.pk
                try:
                    columns = json.loads(right_dataset.columns) or []
                except json.JSONDecodeError as json_err:
                    logger.error('Error on parsing json data of dataset columns.')
                    columns = []
                if right_dataset.dataset.index_field is not None and right_dataset.dataset.index_field not in columns:
                    columns.append(right_dataset.dataset.index_field)
                if right_dataset.dataset.entity_field is not None and right_dataset.dataset.entity_field not in columns:
                    columns.append(right_dataset.dataset.entity_field)
                self.fields['right_columns'].initial = columns
            except LinkingProject.DoesNotExist:
                logger.error('Database error. Linking project with id {0} was not found'.format(self.instance.pk))
                pass


class DedupForm(ProjectForm):
    left_data = ModelChoiceField(queryset=Dataset.objects.all(), label='Data file',
                                 widget=Select(attrs={'class': 'form-control'}))

    class Meta(ProjectForm.Meta):
        fields = ProjectForm.Meta.fields

        labels = ProjectForm.Meta.labels

        widgets = ProjectForm.Meta.widgets


LinkingStepFormset = inlineformset_factory(
    LinkingProject,
    LinkingStep,
    fields=('seq', 'blocking_schema', 'linking_schema', 'group', 'linking_method'),
    widgets={
        'seq': HiddenInput(attrs={'class': 'step-seq form-control'}),
        'blocking_schema': HiddenInput(),
        'linking_schema': HiddenInput(),
        'group': CheckboxInput(attrs={'class': 'ios-toggle toggle-info form-control'}),
        'linking_method': Select(attrs={'class': 'form-control link-method'}),
    },
    labels={
        'seq': _('Sequence'),
        'group': _('Group Records?'),
        'linking_method': _('Linking Method'),
    },
    extra=0
)
