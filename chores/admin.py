from django.contrib import admin

from .models import Chore, CompletionLog, Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Chore)
class ChoreAdmin(admin.ModelAdmin):
    list_display = ("title", "assigned_member", "due_date", "recurrence_days")
    list_filter = ("assigned_member",)


@admin.register(CompletionLog)
class CompletionLogAdmin(admin.ModelAdmin):
    list_display = ("chore", "completed_by", "completed_at")
