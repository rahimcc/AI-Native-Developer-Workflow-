from datetime import timedelta

from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ChoreForm, MemberForm
from .models import Chore, CompletionLog, Member


def member_list(request):
    members = Member.objects.order_by("name")
    return render(request, "chores/member_list.html", {"members": members})


def member_add(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("chores:member_list")
    else:
        form = MemberForm()
    return render(request, "chores/member_form.html", {"form": form})


def member_edit(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == "POST":
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect("chores:member_list")
    else:
        form = MemberForm(instance=member)
    return render(request, "chores/member_form.html", {"form": form, "member": member})


def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == "POST":
        member.delete()
        return redirect("chores:member_list")
    return render(request, "chores/member_confirm_delete.html", {"member": member})


def chore_list(request):
    chores = Chore.objects.select_related("assigned_member").all()

    member_id = request.GET.get("member") or ""
    if member_id:
        chores = chores.filter(assigned_member_id=member_id)

    sort = request.GET.get("sort") or "due_date"
    if sort == "member":
        chores = chores.order_by("assigned_member__name", "due_date")
    else:
        sort = "due_date"
        chores = chores.order_by("due_date")

    context = {
        "chores": chores,
        "members": Member.objects.order_by("name"),
        "selected_member": member_id,
        "sort": sort,
    }
    return render(request, "chores/chore_list.html", context)


def chore_add(request):
    if request.method == "POST":
        form = ChoreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("chores:chore_list")
    else:
        form = ChoreForm()
    return render(request, "chores/chore_form.html", {"form": form})


def chore_edit(request, pk):
    chore = get_object_or_404(Chore, pk=pk)
    if request.method == "POST":
        form = ChoreForm(request.POST, instance=chore)
        if form.is_valid():
            form.save()
            return redirect("chores:chore_list")
    else:
        form = ChoreForm(instance=chore)
    return render(request, "chores/chore_form.html", {"form": form, "chore": chore})


def chore_delete(request, pk):
    chore = get_object_or_404(Chore, pk=pk)
    if request.method == "POST":
        chore.delete()
        return redirect("chores:chore_list")
    return render(request, "chores/chore_confirm_delete.html", {"chore": chore})


@require_POST
def chore_complete(request, pk):
    chore = get_object_or_404(Chore, pk=pk)
    CompletionLog.objects.create(chore=chore, completed_by=chore.assigned_member)

    if chore.recurrence_days:
        chore.due_date = chore.due_date + timedelta(days=chore.recurrence_days)
        chore.save()
    else:
        chore.delete()

    return redirect("chores:chore_list")
