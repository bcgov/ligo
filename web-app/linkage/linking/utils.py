import json
import logging
from django.forms.models import model_to_dict
from django.conf import settings
from .models import LinkingProject, LinkingDataset

logger = logging.getLogger(__name__)

def project_to_json(project_id):

    def get_column_dict(data_dict, columns):
        columns_dict = {}
        if data_dict:
            for (key, value) in data_dict.items():
                if key in columns:
                    columns_dict[key] = value
        return columns_dict

    project = LinkingProject.objects.get(pk=project_id)
    project_json = model_to_dict(project)

    link_datasets = project.linkingdataset_set.all().order_by('link_seq')
    project_json['steps'] = [model_to_dict(step) for step in project.steps.all()]
    project_json['datasets'] = [model_to_dict(rec.dataset) for rec in link_datasets]
    datasets = project_json['datasets']
    if len(datasets) > 0:
        left_link = LinkingDataset.objects.get(link_project=project, link_seq=1)
        try:
            left_columns = json.loads(left_link.columns) or []
        except json.JSONDecodeError as json_err:
            logger.error('Error on parsing json data of dataset columns.')
            left_columns = []

        datasets[0]['columns'] = left_columns
        datasets[0]['data_types'] = get_column_dict(datasets[0]['data_types'], left_columns)
        datasets[0]['field_cats'] = get_column_dict(datasets[0]['field_cats'], left_columns)

    if len(datasets) > 1 and project.type == 'LINK':
        right_link = LinkingDataset.objects.get(link_project=project, link_seq=2)
        try:
            right_columns = json.loads(right_link.columns) or []
        except json.JSONDecodeError as json_err:
            logger.error('Error on parsing dataset columns json.')
            right_columns = []

        datasets[1]['columns'] = right_columns
        datasets[1]['data_types'] = get_column_dict(datasets[1]['data_types'], right_columns)
        datasets[0]['field_cats'] = get_column_dict(datasets[1]['field_cats'], right_columns)

    for dataset in project_json.get('datasets', []):
        dataset['url'] = settings.DATASTORE_URL + dataset['url']
        del dataset['id']

    for step in project_json['steps']:
        del step['id']
        del step['linking_project']

    project_json['output_root'] = settings.OUTPUT_URL
    project_json['temp_path'] = settings.LINKING_TEMP_PATH

    del project_json['id']
    if project.type == 'DEDUP':
        del project_json['relationship_type']

    return project_json

