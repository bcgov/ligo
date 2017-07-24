from __future__ import unicode_literals, absolute_import

import pandas as pd
import numpy as np
from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django.contrib.postgres.fields import JSONField


COPLUMN_TYPES = (
    ('BOOLEAN', 'Boolean'),
    ('REAL', 'Float'),
    ('INTEGER', 'Integer'),
    ('VARCHAR', 'String'),
)


@python_2_unicode_compatible
class Dataset(models.Model):

    dataset_formats = (
        ('CSV', 'Comma Separated Values'),
        ('XLSX', 'Microsoft Excel file'),
        ('JSON', 'JavaScript Object Notation'),
        ('XML', 'XML')
    )

    name = models.CharField(_('Name of Dataset'), unique=True, max_length=255)
    title = models.CharField(_('Title of Dataset'), max_length=1024)
    description = models.TextField(_('Dataset description'), null=True, blank=True)
    format = models.CharField(_('Dataset Format'), max_length=6, choices=dataset_formats, default='CSV')
    index_field = models.CharField(_('Index Field'), default='id', max_length=255)
    entity_field = models.CharField(_('Entity identifier Field'), default='entity_id', max_length=255)
    url = models.CharField(_('Name of the dataset file'), max_length=255)

    data_types = JSONField(blank=True, null=True)
    field_cats = JSONField(blank=True, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

    def get_fields(self):
        if self.data_types:
            return list(self.data_types.keys())
        else:
            file_path = settings.DATASTORE_URL + self.url
            df = pd.read_csv(file_path, nrows=1)
            return list(df)


    def get_absolute_url(self):
        return reverse("datasets:edit", kwargs={"pk": self.pk})



