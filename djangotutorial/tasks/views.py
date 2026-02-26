from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from .models import Task
from .forms import TaskForm


class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.GET.get('status')
        priority_filter = self.request.GET.get('priority')

        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_tasks = Task.objects.all()
        context['total_count'] = all_tasks.count()
        context['todo_count'] = all_tasks.filter(status=Task.Status.TODO).count()
        context['in_progress_count'] = all_tasks.filter(status=Task.Status.IN_PROGRESS).count()
        context['done_count'] = all_tasks.filter(status=Task.Status.DONE).count()
        context['current_status'] = self.request.GET.get('status', '')
        context['current_priority'] = self.request.GET.get('priority', '')
        return context


class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Create New Task'
        context['submit_label'] = 'Create Task'
        return context


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'Edit: {self.object.title}'
        context['submit_label'] = 'Save Changes'
        return context


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks:list')
    context_object_name = 'task'


def toggle_status(request, pk):
    """Toggle task status: TODO -> IN_PROGRESS -> DONE -> TODO."""
    task = get_object_or_404(Task, pk=pk)
    task.status = task.next_status
    task.save()
    return redirect('tasks:list')
