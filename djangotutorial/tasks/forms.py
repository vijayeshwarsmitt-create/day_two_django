from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter task title...',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Describe the task...',
                'rows': 4,
            }),
            'status': forms.Select(attrs={
                'class': 'form-input',
            }),
            'priority': forms.Select(attrs={
                'class': 'form-input',
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
            }),
        }
