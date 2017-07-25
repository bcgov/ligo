import json
import logging
import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from linkage.datasets.models import Dataset
from linkage.linking.utils import project_to_json
from linkage.taskapp.tasks import (run_task,
                                   get_task_result,
                                   linkage_algorithms, TaskStatus)

from .forms import LinkingForm, DedupForm, LinkingStepFormset, ProjectTypeForm
from .models import (LinkingProject,
                     LinkingStep,
                     LinkingDataset)

logger = logging.getLogger(__name__)

algorithms = linkage_algorithms()
BLOKING_COMPARISONS = algorithms.get('blocking')
LINKING_COMPARISONS = algorithms.get('linking')
COMPARISON_ARGS = algorithms.get('args')


def select_type(request):
    if request.method == 'POST':
        form = ProjectTypeForm(request.POST)
        if form.is_valid():
            type = form.cleaned_data['type']
            return HttpResponseRedirect(reverse('linking:add', kwargs={'type': type}))
    else:
        form = ProjectTypeForm()

    return render(request, 'linking/project_type_select.html', {'form': form})


def update_status(project):
    """
    Checks the running project status and updates the status and adds the result if the project is completed.
    :param project: The current running project.
    :return: Nothing
    """
    logger.debug('>>--- update_status --->>')
    logger.debug('Project task_id : {0}'.format(project.task_id))

    # Get task result (Summary report file)
    task_status, result = get_task_result(project.task_id)

    logger.debug('Project Status : {0}, Result: {1}.'.format(task_status, result))

    if task_status == TaskStatus.PENDING:
        logger.debug('<<--- update_status ---<<')
        return

    if task_status == TaskStatus.DONE and result is not None:
        project.results_file = result
        project.status = 'COMPLETED'
    else:
        project.status = 'FAILED'
        project.comments = 'An error occurred during project execution. Please check the logs for details'

    project.save()

    logger.debug('<<--- update_status ---<<')


class ProjectsListMixin(object):
    def get_context_data(self, **kwargs):
        '''
        Gets the total number of projects in running state and adds it to response data.
        :param kwargs:
        :return: Response context
        '''
        data = super(ProjectsListMixin, self).get_context_data(**kwargs)
        running_projects = LinkingProject.objects.filter(status='RUNNING')

        for project in running_projects:
            update_status(project)

        total_running = LinkingProject.objects.filter(status='RUNNING').count()
        logger.info('Number of projects currently running: {0}'.format(total_running))

        data['total_running'] = total_running

        return data


class LinkingProjectListView(LoginRequiredMixin, ProjectsListMixin, ListView):
    model = LinkingProject


class AjaxListView(LoginRequiredMixin, ProjectsListMixin, ListView):
    model = LinkingProject
    template_name = 'linking/projects_list.html'


class LinkingProjectCreateView(LoginRequiredMixin, CreateView):
    model = LinkingProject

    form_class = LinkingForm
    template_name = 'linking/linkingproject_form.html'

    def form_valid(self, form):
        form.instance.type = 'LINK'
        new_project = form.save()

        # Save linking project data files
        left_dataset = Dataset.objects.get(pk=form.cleaned_data['left_data'].pk)
        left_link = LinkingDataset(link_project=new_project,
                                   dataset=left_dataset,
                                   link_seq=1)
        left_link.save()

        right_dataset = Dataset.objects.get(pk=form.cleaned_data['right_data'].pk)
        right_link = LinkingDataset(link_project=new_project,
                                    dataset=right_dataset,
                                    link_seq=2)
        right_link.save()

        return super(LinkingProjectCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('linking:edit', kwargs={'type': self.object.type, 'pk': self.object.pk})


class DedupProjectCreateView(LoginRequiredMixin, CreateView):
    model = LinkingProject

    form_class = DedupForm

    template_name = 'linking/dedupproject_form.html'

    def form_valid(self, form):
        form.instance.type = 'DEDUP'
        new_project = form.save()

        # Save linking project data files
        left_dataset = Dataset.objects.get(pk=form.cleaned_data['left_data'].pk)
        left_link = LinkingDataset(link_project=new_project,
                                   dataset=left_dataset,
                                   link_seq=1)
        left_link.save()

        return super(DedupProjectCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('linking:edit', kwargs={'type': self.object.type, 'pk': self.object.pk})


def create_project(request, type):
    '''
    Calls the corresponding project create view depending on the project type
    :param request: project create request
    :param type: TYpe of the project. Values: LINK, DEDUP
    :return:
    '''
    if type == 'LINK':
        return LinkingProjectCreateView.as_view()(request)
    else:
        return DedupProjectCreateView.as_view()(request)


class ProjectUpdateMixin(object):
    def get_context_data(self, **kwargs):
        data = super(ProjectUpdateMixin, self).get_context_data(**kwargs)
        if self.request.POST:
            data['linking_step_form'] = LinkingStepFormset(self.request.POST, instance=self.object)
        else:
            linking_step_form = LinkingStepFormset(instance=self.object)

            data['linking_step_form'] = linking_step_form
            data['blocking_transformation_choices'] = BLOKING_COMPARISONS
            data['linking_comparison_choices'] = LINKING_COMPARISONS
            data['comparison_args'] = COMPARISON_ARGS
            data['type'] = self.object.type
            left_link = LinkingDataset.objects.get(link_project=self.object, link_seq=1)
            required_left = []
            if left_link:
                required_left.append(left_link.dataset.index_field)
                entity_id = left_link.dataset.entity_field
                if entity_id:
                    required_left.append(entity_id)
            data['required_left'] = required_left

            if self.object.type == 'LINK':
                right_link = LinkingDataset.objects.get(link_project=self.object, link_seq=2)
                required_right = []
                if right_link:
                    required_right.append(right_link.dataset.index_field)
                    entity_id = right_link.dataset.entity_field
                    if entity_id:
                        required_right.append(entity_id)

                data['required_right'] = required_right


        return data

    def form_valid(self, form):

        context = self.get_context_data()
        linking_step_form = context['linking_step_form']
        if linking_step_form.is_valid():
            self.object = form.save()

            self.object.save()
            linking_step_form.instance = self.object
            i = 1
            for item in linking_step_form:
                item['seq'].value = i
                i += 1
            linking_step_form.save()

            left_link = LinkingDataset.objects.get(link_project=self.object, link_seq=1)
            if left_link:
                left_link.columns = form.cleaned_data['left_columns']
                left_link.dataset = Dataset.objects.get(pk=form.cleaned_data['left_data'].pk)
                left_link.save()

            if self.object.type == 'LINK':
                right_link = LinkingDataset.objects.get(link_project=self.object, link_seq=2)
                if right_link:
                    right_link.columns = form.cleaned_data['right_columns']
                    right_link.dataset = Dataset.objects.get(pk=form.cleaned_data['right_data'].pk)
                    right_link.save()

        return super(ProjectUpdateMixin, self).form_valid(form)

    def get_success_url(self):
        return reverse('linking:list')


class LinkingProjectUpdateView(LoginRequiredMixin, ProjectUpdateMixin, UpdateView):
    model = LinkingProject

    form_class = LinkingForm
    template_name = 'linking/linkingproject_form.html'

    def get_context_data(self, **kwargs):
        data = super(LinkingProjectUpdateView, self).get_context_data(**kwargs)
        if not self.request.POST:
            linking_step_form = data['linking_step_form']
            steps = LinkingStep.objects.filter(linking_project=self.object).order_by('seq').values()

            blocking_schema = {}
            linking_schema = {}
            for item in linking_step_form:
                seq = item['seq'].value()
                if seq:
                    step = steps.filter(seq=seq)
                    block_schema = step.first()['blocking_schema']
                    link_schema = step.first()['linking_schema']
                    blocking_schema[seq] = zip(block_schema['left'],
                                               block_schema['right'],
                                               block_schema['transformations'])

                    linking_schema[seq] = zip(link_schema['left'],
                                              link_schema['right'],
                                              link_schema['comparisons'])
            data['blocking_schema'] = blocking_schema
            data['linking_schema'] = linking_schema

        return data


class DedupProjectUpdateView(LoginRequiredMixin, ProjectUpdateMixin, UpdateView):
    model = LinkingProject

    form_class = DedupForm
    template_name = 'linking/dedupproject_form.html'

    def get_context_data(self, **kwargs):
        data = super(DedupProjectUpdateView, self).get_context_data(**kwargs)
        if not self.request.POST:
            linking_step_form = data['linking_step_form']
            steps = LinkingStep.objects.filter(linking_project=self.object).order_by('seq').values()

            blocking_schema = {}
            linking_schema = {}
            for item in linking_step_form:
                seq = item['seq'].value()
                if seq:
                    step = steps.filter(seq=seq)
                    block_schema = step.first()['blocking_schema']
                    link_schema = step.first()['linking_schema']
                    blocking_schema[seq] = zip(block_schema['left'],
                                               block_schema['right'],
                                               block_schema['transformations'])

                    linking_schema[seq] = zip(link_schema['left'],
                                              link_schema['right'],
                                              link_schema['comparisons'])
            data['blocking_schema'] = blocking_schema
            data['linking_schema'] = linking_schema

        return data


def edit_project(request, type, pk):
    logger.debug(request)
    if type == 'LINK':
        return LinkingProjectUpdateView.as_view()(request, pk=pk)
    else:
        return DedupProjectUpdateView.as_view()(request, pk=pk)


class LinkingProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = LinkingProject

    form_class = LinkingForm

    def get_success_url(self):
        return reverse('linking:list')


@transaction.non_atomic_requests
@csrf_protect
@login_required
def execute(request, pk):
    """
    Runs a linking/De-Diplication job in background without blocking user actions.
    :param request:
    :param name: Project name
    :return:
    """

    project_json = project_to_json(pk)

    print (project_json)
    try:
        project = None
        project = LinkingProject.objects.get(pk=pk)

        name = project.name

        logger.debug("name : {0}".format(name))
        logger.debug("project_json : {0}".format(project_json))

        project.status = 'RUNNING'

        logger.debug("project : {0}".format(project))

        task = run_task(name, project_json)
        logger.debug(task.id)
        project.task_id = task.id
        project.save()
    except LinkingProject.DoesNotExist as db_err:
        logger.error('Database error. Linking project with id {0} was not found.'.format(pk))
    except Exception as e:
        if project is not None:
            project.status = 'FAILED'

            project.save()

    return HttpResponseRedirect(reverse('linking:list'))


def view_results(request, pk):
    try:
        project = LinkingProject.objects.get(pk=pk)
        project_type = {'LINK': 'Linking', 'DEDUP': 'De-Duplication'}.get(project.type, '')
        file_path = project.results_file
        results_file = os.path.basename(file_path)
        logger.debug(file_path)
        # Adding file name for ease of debugging
        if not os.path.exists(file_path):
            message = project_type \
                      + ' Results summary file was not found. The file must have been deleted. ' \
                      + 'Please rerun the project to genereate the file.'
            return render(request, 'linking/linking_errors.html', {'message': message})

        # Binary mode should be specified in Python 3 otherwise we would get encoding error
        with open(file_path, 'r+b') as report:
            response = HttpResponse(report.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline;filename=' + results_file
            return response
    except LinkingProject.DoesNotExist:
        logger.error('Database Error: Linking project with id {0} was not found.'.format(pk))
        return HttpResponseRedirect(reverse('linking:list'))


def stop_project(request, pk):
    try:
        project = LinkingProject.objects.get(pk=pk)
        project.status = 'READY'
        project.save()

    except LinkingProject.DoesNotExist as db_err:
        logger.error('Database Error: Linking project with id {0} was not found.'.format(pk))

    return HttpResponseRedirect(reverse('linking:list'))


def export_to_json(request, pk):

    project_json = project_to_json(pk)

    return HttpResponse(json.dumps(project_json), content_type="application/json")
