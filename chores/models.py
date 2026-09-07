from django.core.validators import MinValueValidator
from django.db import models


class Member(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Chore(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assigned_member = models.ForeignKey(
        Member, on_delete=models.SET_NULL, null=True, blank=True, related_name="chores"
    )
    recurrence_days = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="Repeat every N days (e.g. 1=daily, 7=weekly). Leave blank for a one-off chore.",
    )
    due_date = models.DateField()

    def __str__(self):
        return self.title


class CompletionLog(models.Model):
    chore = models.ForeignKey(
        Chore, on_delete=models.SET_NULL, null=True, blank=True, related_name="completions"
    )
    chore_title = models.CharField(max_length=200, blank=True)
    completed_by = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.chore_title and self.chore_id:
            self.chore_title = self.chore.title
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.chore_title or 'Unknown chore'} completed at {self.completed_at:%Y-%m-%d %H:%M}"
