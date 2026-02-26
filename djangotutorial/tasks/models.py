from django.db import models
from django.urls import reverse


class Task(models.Model):
    class Status(models.TextChoices):
        TODO = 'TODO', 'To Do'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        DONE = 'DONE', 'Done'

    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO,
    )
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tasks:detail', kwargs={'pk': self.pk})

    @property
    def next_status(self):
        """Return the next status in the cycle: TODO -> IN_PROGRESS -> DONE -> TODO."""
        cycle = {
            self.Status.TODO: self.Status.IN_PROGRESS,
            self.Status.IN_PROGRESS: self.Status.DONE,
            self.Status.DONE: self.Status.TODO,
        }
        return cycle.get(self.status, self.Status.TODO)

    @property
    def is_overdue(self):
        """Check if the task is overdue."""
        if self.due_date and self.status != self.Status.DONE:
            from django.utils import timezone
            return self.due_date < timezone.now().date()
        return False
